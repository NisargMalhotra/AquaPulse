"""
AquaPulse – Analytics & Prediction Engine
==========================================
Business-logic layer implementing:

* **Toxicity Index** – per-parameter and aggregate health scoring.
* **Emergency Water Change Calculator** – dilution math (C₁V₁ = C₂V₂).
* **Predictive Maintenance** – dNO₃⁻/dt via ``numpy.gradient`` with
  extrapolation to the mandatory water-change threshold.
* **Stability Metrics** – 7-day / 14-day rolling averages and σ for
  pH and temperature.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from utils.constants import (
    HealthStatus,
    NITRATE_CHANGE_THRESHOLD,
    TAP_WATER_DEFAULTS,
    TARGET_SAFE,
    THRESHOLDS,
)


# ─── Data-Transfer Objects ──────────────────────────────────────────────────────


@dataclass
class ParameterStatus:
    """Health evaluation result for a single water parameter."""

    name: str
    value: float
    status: HealthStatus
    message: str


@dataclass
class ToxicityReport:
    """Aggregated toxicity report for an entire set of readings."""

    overall_status: HealthStatus
    parameters: List[ParameterStatus] = field(default_factory=list)
    toxicity_score: float = 0.0  # 0 (pristine) → 100 (lethal)


@dataclass
class WaterChangeRecommendation:
    """Recommended dilution to restore safe water parameters."""

    needed: bool
    change_pct: float  # % of tank volume to replace
    limiting_parameter: str
    details: Dict[str, float] = field(default_factory=dict)


@dataclass
class MaintenancePrediction:
    """Predictive-maintenance output."""

    nitrate_rate_ppm_per_day: Optional[float]
    days_until_threshold: Optional[float]
    current_nitrate: Optional[float]
    threshold: float = NITRATE_CHANGE_THRESHOLD
    confidence: str = "Low"  # Low / Medium / High


@dataclass
class StabilityMetrics:
    """Rolling-window statistics for pH and temperature."""

    ph_mean_7d: Optional[float] = None
    ph_std_7d: Optional[float] = None
    ph_mean_14d: Optional[float] = None
    ph_std_14d: Optional[float] = None
    temp_mean_7d: Optional[float] = None
    temp_std_7d: Optional[float] = None
    temp_mean_14d: Optional[float] = None
    temp_std_14d: Optional[float] = None


# ─── Engine ─────────────────────────────────────────────────────────────────────


class AnalyticsEngine:
    """Core analytics and prediction logic for AquaPulse."""

    # ── Toxicity Assessment ──────────────────────────────────────────────

    @staticmethod
    def evaluate_parameter(name: str, value: float) -> ParameterStatus:
        """
        Evaluate a single parameter against its safety thresholds.

        Args:
            name:  Column name matching a key in ``THRESHOLDS``
                   (e.g. ``"ammonia_ppm"``).
            value: Current measured value.

        Returns:
            A :class:`ParameterStatus` with the computed health level.
        """
        thresholds = THRESHOLDS.get(name, {})

        # ── Upper-bound-only parameters (ammonia, nitrite, nitrate) ──
        if "safe_min" not in thresholds:
            safe_max = thresholds.get("safe_max", float("inf"))
            warning_max = thresholds.get("warning_max", float("inf"))

            if value <= safe_max:
                status = HealthStatus.SAFE
                msg = f"{value:.2f} ppm — within safe range"
            elif value <= warning_max:
                status = HealthStatus.WARNING
                msg = f"{value:.2f} ppm — elevated, monitor closely"
            else:
                status = HealthStatus.CRITICAL
                msg = f"{value:.2f} ppm — CRITICAL, immediate action required"

        # ── Range-bound parameters (pH, temperature) ─────────────────
        else:
            safe_min = thresholds["safe_min"]
            safe_max = thresholds["safe_max"]
            warn_min = thresholds.get("warning_min", safe_min)
            warn_max = thresholds.get("warning_max", safe_max)
            unit = "°C" if "temp" in name else ""

            if safe_min <= value <= safe_max:
                status = HealthStatus.SAFE
                msg = f"{value:.1f}{unit} — stable and within ideal range"
            elif warn_min <= value <= warn_max:
                status = HealthStatus.WARNING
                msg = f"{value:.1f}{unit} — outside ideal range, monitor trend"
            else:
                status = HealthStatus.CRITICAL
                msg = f"{value:.1f}{unit} — CRITICAL deviation detected"

        return ParameterStatus(name=name, value=value, status=status, message=msg)

    @classmethod
    def generate_toxicity_report(
        cls,
        reading: Dict[str, float],
    ) -> ToxicityReport:
        """
        Build a comprehensive toxicity report from a single reading dict.

        The **toxicity score** is a weighted average (0–100) where:
        - Safe = 0, Warning = 50, Critical = 100
        - Weights: NH₃ 40 %, NO₂⁻ 30 %, NO₃⁻ 15 %, pH 10 %, Temp 5 %

        The **overall status** equals the worst individual status.
        """
        score_weights: Dict[str, int] = {
            "ammonia_ppm": 40,
            "nitrite_ppm": 30,
            "nitrate_ppm": 15,
            "ph": 10,
            "temperature_c": 5,
        }
        status_score_map = {
            HealthStatus.SAFE: 0,
            HealthStatus.WARNING: 50,
            HealthStatus.CRITICAL: 100,
        }

        params: List[ParameterStatus] = []
        weighted_sum = 0.0
        total_weight = 0.0
        worst = HealthStatus.SAFE

        for param_name, weight in score_weights.items():
            value = reading.get(param_name)
            if value is None:
                continue

            ps = cls.evaluate_parameter(param_name, float(value))
            params.append(ps)

            weighted_sum += status_score_map[ps.status] * weight
            total_weight += weight

            if ps.status == HealthStatus.CRITICAL:
                worst = HealthStatus.CRITICAL
            elif (
                ps.status == HealthStatus.WARNING
                and worst != HealthStatus.CRITICAL
            ):
                worst = HealthStatus.WARNING

        toxicity = (weighted_sum / total_weight) if total_weight else 0.0

        return ToxicityReport(
            overall_status=worst,
            parameters=params,
            toxicity_score=round(toxicity, 1),
        )

    # ── Emergency Water-Change Calculator ────────────────────────────────

    @staticmethod
    def calculate_water_change(
        current: Dict[str, float],
        target: Optional[Dict[str, float]] = None,
        tap_water: Optional[Dict[str, float]] = None,
    ) -> WaterChangeRecommendation:
        """
        Calculate the minimum % water change required to reach safe levels.

        Uses the dilution equation:

            C_final = (1 − X) · C_current  +  X · C_tap

        Solving for the fraction *X* to replace:

            X = (C_current − C_target) / (C_current − C_tap)

        The **limiting parameter** (requiring the largest change) determines
        the recommendation.

        Args:
            current:   Dict of current concentrations (ppm keys).
            target:    Target concentrations after dilution.
            tap_water: Assumed tap-water concentrations.

        Returns:
            A :class:`WaterChangeRecommendation`.
        """
        target = target or TARGET_SAFE
        tap_water = tap_water or TAP_WATER_DEFAULTS

        details: Dict[str, float] = {}
        max_change = 0.0
        limiting = ""

        for param in ("ammonia_ppm", "nitrite_ppm", "nitrate_ppm"):
            c_cur = current.get(param, 0.0)
            c_tgt = target.get(param, 0.0)
            c_tap = tap_water.get(param, 0.0)

            if c_cur <= c_tgt:
                details[param] = 0.0
                continue

            denom = c_cur - c_tap
            if denom <= 0:
                # Tap water is equal or worse — dilution won't help
                details[param] = 100.0
            else:
                frac = (c_cur - c_tgt) / denom
                details[param] = round(min(max(frac * 100, 0), 100), 1)

            if details[param] > max_change:
                max_change = details[param]
                limiting = param

        return WaterChangeRecommendation(
            needed=max_change > 0,
            change_pct=round(max_change, 1),
            limiting_parameter=limiting,
            details=details,
        )

    # ── Predictive Maintenance ───────────────────────────────────────────

    @staticmethod
    def predict_maintenance(
        df: pd.DataFrame,
        threshold: float = NITRATE_CHANGE_THRESHOLD,
    ) -> MaintenancePrediction:
        """
        Estimate nitrate accumulation rate and project the number of
        **days until the mandatory water-change threshold** is reached.

        Rate of change is calculated as:

            d[NO₃⁻] / dt   (ppm / day)

        using :func:`numpy.gradient` over the most recent readings that
        were *not* preceded by a water change, averaged over the last
        five data points for smoothing.

        Args:
            df:        DataFrame with at least ``timestamp``,
                       ``nitrate_ppm``, and ``water_changed`` columns.
            threshold: Nitrate level (ppm) that triggers a change.

        Returns:
            A :class:`MaintenancePrediction`.
        """
        if df.empty or len(df) < 2:
            return MaintenancePrediction(
                nitrate_rate_ppm_per_day=None,
                days_until_threshold=None,
                current_nitrate=(
                    float(df["nitrate_ppm"].iloc[-1]) if not df.empty else None
                ),
            )

        # Prefer non-water-change readings for a cleaner trend
        trend_df = df[df["water_changed"] == 0].copy()
        if len(trend_df) < 2:
            trend_df = df.copy()

        timestamps = pd.to_datetime(trend_df["timestamp"])
        days_elapsed = (
            (timestamps - timestamps.iloc[0]).dt.total_seconds() / 86_400.0
        )
        no3_values = trend_df["nitrate_ppm"].values.astype(float)

        # numpy gradient → instantaneous rate at each sample
        d_days = days_elapsed.values
        if len(d_days) >= 2:
            gradients = np.gradient(no3_values, d_days)
            recent = min(5, len(gradients))
            rate = float(np.mean(gradients[-recent:]))
        else:
            rate = 0.0

        current_no3 = float(df["nitrate_ppm"].iloc[-1])

        # Project days remaining
        if rate > 0 and current_no3 < threshold:
            days_remaining: Optional[float] = (threshold - current_no3) / rate
        elif current_no3 >= threshold:
            days_remaining = 0.0
        else:
            days_remaining = None  # decreasing / stable → no action needed

        # Confidence level
        n = len(trend_df)
        if n >= 14:
            confidence = "High"
        elif n >= 7:
            confidence = "Medium"
        else:
            confidence = "Low"

        return MaintenancePrediction(
            nitrate_rate_ppm_per_day=round(rate, 3),
            days_until_threshold=(
                round(days_remaining, 1) if days_remaining is not None else None
            ),
            current_nitrate=round(current_no3, 2),
            threshold=threshold,
            confidence=confidence,
        )

    # ── Stability Metrics ────────────────────────────────────────────────

    @staticmethod
    def calculate_stability(df: pd.DataFrame) -> StabilityMetrics:
        """
        Compute 7-day and 14-day rolling averages and standard deviations
        for pH and temperature.

        If fewer readings than the window size exist, all available
        readings are used.
        """
        metrics = StabilityMetrics()
        if df.empty:
            return metrics

        sdf = df.copy()
        sdf["timestamp"] = pd.to_datetime(sdf["timestamp"])
        sdf = sdf.sort_values("timestamp")

        for window, suffix in [(7, "7d"), (14, "14d")]:
            window_df = sdf.tail(window) if len(sdf) >= window else sdf

            ph_mean = float(window_df["ph"].mean())
            ph_std = (
                float(window_df["ph"].std()) if len(window_df) > 1 else 0.0
            )
            temp_mean = float(window_df["temperature_c"].mean())
            temp_std = (
                float(window_df["temperature_c"].std())
                if len(window_df) > 1
                else 0.0
            )

            setattr(metrics, f"ph_mean_{suffix}", round(ph_mean, 2))
            setattr(metrics, f"ph_std_{suffix}", round(ph_std, 3))
            setattr(metrics, f"temp_mean_{suffix}", round(temp_mean, 2))
            setattr(metrics, f"temp_std_{suffix}", round(temp_std, 3))

        return metrics

    @staticmethod
    def get_rolling_dataframe(
        df: pd.DataFrame,
        window: int = 7,
    ) -> pd.DataFrame:
        """
        Return a *copy* of *df* with added rolling-mean and rolling-std
        columns for ``ph`` and ``temperature_c``.

        New columns follow the pattern
        ``ph_rolling_mean_7d``, ``ph_rolling_std_7d``, etc.
        """
        if df.empty:
            return df.copy()

        result = df.copy()
        result["timestamp"] = pd.to_datetime(result["timestamp"])
        result = result.sort_values("timestamp").reset_index(drop=True)

        min_periods = min(2, window)

        for col, prefix in [("ph", "ph"), ("temperature_c", "temp")]:
            result[f"{prefix}_rolling_mean_{window}d"] = (
                result[col]
                .rolling(window=window, min_periods=min_periods)
                .mean()
            )
            result[f"{prefix}_rolling_std_{window}d"] = (
                result[col]
                .rolling(window=window, min_periods=min_periods)
                .std()
            )

        return result
