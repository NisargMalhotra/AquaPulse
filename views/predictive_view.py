"""
AquaPulse – Predictive Maintenance Panel
=========================================
Visual KPI cards showing:

* Per-parameter health status (Safe / Warning / Critical).
* Current nitrate accumulation rate (ppm/day).
* Estimated countdown to the next mandatory water change.
* Emergency water-change recommendation (% to replace).
* 7-day / 14-day pH and temperature stability metrics.
"""

import customtkinter as ctk
import pandas as pd

from controllers.analytics_engine import (
    AnalyticsEngine,
    MaintenancePrediction,
    StabilityMetrics,
    ToxicityReport,
    WaterChangeRecommendation,
)
from models.database import DatabaseManager
from utils.constants import Colors, HealthStatus


class PredictiveView(ctk.CTkFrame):
    """Predictive maintenance panel with colour-coded KPI cards."""

    def __init__(
        self,
        parent: ctk.CTkFrame,
        db: DatabaseManager,
        engine: AnalyticsEngine,
    ) -> None:
        super().__init__(parent, fg_color=Colors.BG_DARK)
        self.db = db
        self.engine = engine
        self.kpi_cards: dict[str, ctk.CTkFrame] = {}
        self._build_ui()

    # ─── UI Construction ─────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """Assemble header, banner, KPI grid, and prediction rows."""
        # ── Header ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(28, 8))

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.pack(fill="x")

        ctk.CTkLabel(
            title_row,
            text="🔮 Predictive Maintenance",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=Colors.TEXT_PRIMARY,
        ).pack(side="left")

        ctk.CTkButton(
            title_row,
            text="🔄 Refresh",
            font=ctk.CTkFont(size=13),
            width=100,
            height=34,
            corner_radius=8,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.ACCENT_BLUE,
            text_color=Colors.TEXT_PRIMARY,
            command=self.on_show,
        ).pack(side="right")

        ctk.CTkLabel(
            header,
            text="Real-time water health assessment and maintenance predictions.",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_SECONDARY,
        ).pack(anchor="w", pady=(4, 0))

        # ── Scrollable body ─────────────────────────────────────────
        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=Colors.BG_TERTIARY,
        )
        self.content.pack(fill="both", expand=True, padx=32, pady=12)

        # ── Overall-status banner ───────────────────────────────────
        self._build_banner()

        # ── Per-parameter KPI cards ─────────────────────────────────
        self._section_label("🧪 Parameter Health")
        kpi_grid = ctk.CTkFrame(self.content, fg_color="transparent")
        kpi_grid.pack(fill="x", pady=(0, 16))
        kpi_grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="kpi")

        kpi_defs = [
            ("ammonia", "🧪 Ammonia", "NH₃ ppm"),
            ("nitrite", "⚗️ Nitrite", "NO₂⁻ ppm"),
            ("nitrate", "🔵 Nitrate", "NO₃⁻ ppm"),
            ("ph", "📐 pH Level", "pH"),
            ("temperature", "🌡️ Temperature", "°C"),
        ]
        for idx, (key, title, unit) in enumerate(kpi_defs):
            row, col = divmod(idx, 3)
            card = self._make_card(kpi_grid, title, "—", unit, "—")
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
            self.kpi_cards[key] = card

        # ── Prediction cards ────────────────────────────────────────
        self._section_label("📈 Maintenance Predictions")
        pred_grid = ctk.CTkFrame(self.content, fg_color="transparent")
        pred_grid.pack(fill="x", pady=(0, 16))
        pred_grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="pred")

        self.rate_card = self._make_card(
            pred_grid, "📉 NO₃⁻ Rate", "—", "ppm/day", "—"
        )
        self.rate_card.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

        self.countdown_card = self._make_card(
            pred_grid, "⏰ Days to Change", "—", "days", "—"
        )
        self.countdown_card.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")

        self.wc_card = self._make_card(
            pred_grid, "💧 Water Change Needed", "—", "%", "—"
        )
        self.wc_card.grid(row=0, column=2, padx=6, pady=6, sticky="nsew")

        # ── Stability cards ─────────────────────────────────────────
        self._section_label("📏 Stability Metrics")
        stab_grid = ctk.CTkFrame(self.content, fg_color="transparent")
        stab_grid.pack(fill="x", pady=(0, 16))
        stab_grid.grid_columnconfigure((0, 1), weight=1, uniform="stab")

        self.ph_stab_card = self._make_card(
            stab_grid, "📐 pH Stability (7d)", "—", "", "—"
        )
        self.ph_stab_card.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

        self.temp_stab_card = self._make_card(
            stab_grid, "🌡️ Temp Stability (7d)", "—", "", "—"
        )
        self.temp_stab_card.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")

    # ─── Banner ──────────────────────────────────────────────────────────

    def _build_banner(self) -> None:
        """Create the top-level overall-status banner."""
        self.banner = ctk.CTkFrame(
            self.content,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=12,
            border_width=2,
            border_color=Colors.BORDER,
            height=90,
        )
        self.banner.pack(fill="x", pady=(0, 16))
        self.banner.pack_propagate(False)

        self.banner_emoji = ctk.CTkLabel(
            self.banner, text="⏳", font=ctk.CTkFont(size=36),
        )
        self.banner_emoji.pack(side="left", padx=(20, 12))

        txt = ctk.CTkFrame(self.banner, fg_color="transparent")
        txt.pack(side="left", fill="both", expand=True, pady=12)

        self.banner_title = ctk.CTkLabel(
            txt,
            text="Awaiting Data…",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=Colors.TEXT_PRIMARY,
            anchor="w",
        )
        self.banner_title.pack(anchor="w")

        self.banner_sub = ctk.CTkLabel(
            txt,
            text="Log your first reading to get started.",
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_SECONDARY,
            anchor="w",
        )
        self.banner_sub.pack(anchor="w")

        self.banner_score = ctk.CTkLabel(
            self.banner,
            text="",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=Colors.TEXT_MUTED,
        )
        self.banner_score.pack(side="right", padx=24)

    # ─── Card Factory ────────────────────────────────────────────────────

    @staticmethod
    def _make_card(
        parent: ctk.CTkFrame,
        title: str,
        value: str,
        unit: str,
        status_text: str,
    ) -> ctk.CTkFrame:
        """Build a single KPI card and stash label references on it."""
        card = ctk.CTkFrame(
            parent,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=12,
            border_width=1,
            border_color=Colors.BORDER,
            height=130,
        )
        card.pack_propagate(False)

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_SECONDARY,
        ).pack(anchor="w", padx=14, pady=(12, 2))

        val_lbl = ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=Colors.TEXT_PRIMARY,
        )
        val_lbl.pack(anchor="w", padx=14)
        card._val_label = val_lbl  # type: ignore[attr-defined]

        unit_lbl = ctk.CTkLabel(
            card, text=unit,
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_MUTED,
        )
        unit_lbl.pack(anchor="w", padx=14)
        card._unit_label = unit_lbl  # type: ignore[attr-defined]

        stat_lbl = ctk.CTkLabel(
            card, text=status_text,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=Colors.TEXT_MUTED,
        )
        stat_lbl.pack(anchor="w", padx=14, pady=(2, 8))
        card._status_label = stat_lbl  # type: ignore[attr-defined]

        return card

    @staticmethod
    def _set_card(
        card: ctk.CTkFrame,
        value: str,
        status_text: str,
        status: HealthStatus,
    ) -> None:
        """Update a KPI card's displayed value and colour."""
        colour = {
            HealthStatus.SAFE: Colors.SAFE_GREEN,
            HealthStatus.WARNING: Colors.WARNING_AMBER,
            HealthStatus.CRITICAL: Colors.CRITICAL_RED,
        }.get(status, Colors.TEXT_MUTED)

        card._val_label.configure(text=value, text_color=colour)  # type: ignore[attr-defined]
        card._status_label.configure(text=status_text, text_color=colour)  # type: ignore[attr-defined]

    def _section_label(self, text: str) -> None:
        """Add a bold section heading to the scrollable body."""
        ctk.CTkLabel(
            self.content,
            text=text,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=Colors.ACCENT_BLUE,
        ).pack(anchor="w", pady=(8, 8))

    # ─── Data Refresh ────────────────────────────────────────────────────

    def on_show(self) -> None:
        """Recalculate and repaint every card with the latest data."""
        try:
            df = self.db.get_readings_as_dataframe()
            latest = self.db.get_latest_reading()
        except RuntimeError:
            return

        if not latest or df.empty:
            return

        # ── Toxicity banner ─────────────────────────────────────────
        report = self.engine.generate_toxicity_report(latest)
        self._refresh_banner(report)

        # ── Individual parameters ───────────────────────────────────
        param_keys = {
            "ammonia": "ammonia_ppm",
            "nitrite": "nitrite_ppm",
            "nitrate": "nitrate_ppm",
            "ph": "ph",
            "temperature": "temperature_c",
        }
        for ui_key, db_col in param_keys.items():
            card = self.kpi_cards.get(ui_key)
            if card is None:
                continue
            ps = self.engine.evaluate_parameter(db_col, float(latest[db_col]))
            fmt = f"{ps.value:.2f}" if "ppm" in db_col else f"{ps.value:.1f}"
            self._set_card(card, fmt, ps.status.value, ps.status)

        # ── Predictions ─────────────────────────────────────────────
        self._refresh_predictions(df)

        # ── Water-change recommendation ─────────────────────────────
        self._refresh_wc(latest)

        # ── Stability ───────────────────────────────────────────────
        self._refresh_stability(df)

    # ── Sub-refresh helpers ──────────────────────────────────────────────

    def _refresh_banner(self, report: ToxicityReport) -> None:
        cfg = {
            HealthStatus.SAFE: ("✅", "Ecosystem Healthy", Colors.SAFE_GREEN),
            HealthStatus.WARNING: ("⚠️", "Attention Needed", Colors.WARNING_AMBER),
            HealthStatus.CRITICAL: ("🚨", "Critical — Act Now!", Colors.CRITICAL_RED),
        }
        emoji, title, colour = cfg[report.overall_status]
        safe_count = sum(
            1 for p in report.parameters if p.status == HealthStatus.SAFE
        )
        total = len(report.parameters)

        self.banner_emoji.configure(text=emoji)
        self.banner_title.configure(text=title, text_color=colour)
        self.banner_sub.configure(
            text=(
                f"Toxicity Score: {report.toxicity_score}/100  —  "
                f"{safe_count}/{total} parameters safe"
            ),
        )
        self.banner_score.configure(
            text=f"{report.toxicity_score:.0f}", text_color=colour,
        )
        self.banner.configure(border_color=colour)

    def _refresh_predictions(self, df: pd.DataFrame) -> None:
        pred = self.engine.predict_maintenance(df)

        # Rate card
        if pred.nitrate_rate_ppm_per_day is not None:
            rate_val = f"{pred.nitrate_rate_ppm_per_day:+.3f}"
            if pred.nitrate_rate_ppm_per_day <= 1.0:
                rate_st = HealthStatus.SAFE
            elif pred.nitrate_rate_ppm_per_day <= 3.0:
                rate_st = HealthStatus.WARNING
            else:
                rate_st = HealthStatus.CRITICAL
        else:
            rate_val, rate_st = "—", HealthStatus.SAFE

        self._set_card(
            self.rate_card, rate_val,
            f"Confidence: {pred.confidence}", rate_st,
        )

        # Countdown card
        if pred.days_until_threshold is not None:
            if pred.days_until_threshold <= 0:
                d_val, d_st, d_txt = "NOW", HealthStatus.CRITICAL, "Water change overdue!"
            elif pred.days_until_threshold <= 3:
                d_val = f"{pred.days_until_threshold:.1f}"
                d_st, d_txt = HealthStatus.WARNING, "Change soon"
            else:
                d_val = f"{pred.days_until_threshold:.1f}"
                d_st, d_txt = HealthStatus.SAFE, "On track"
        else:
            d_val, d_st, d_txt = "∞", HealthStatus.SAFE, "Stable / decreasing"

        self._set_card(self.countdown_card, d_val, d_txt, d_st)

    def _refresh_wc(self, latest: dict) -> None:
        rec = self.engine.calculate_water_change(latest)
        if rec.needed:
            val = f"{rec.change_pct:.0f}%"
            st = (
                HealthStatus.WARNING
                if rec.change_pct <= 50
                else HealthStatus.CRITICAL
            )
            txt = f"Limiting: {rec.limiting_parameter.replace('_ppm', '')}"
        else:
            val, st, txt = "0%", HealthStatus.SAFE, "No change needed"
        self._set_card(self.wc_card, val, txt, st)

    def _refresh_stability(self, df: pd.DataFrame) -> None:
        stab = self.engine.calculate_stability(df)

        # pH
        if stab.ph_mean_7d is not None:
            ph_v = f"{stab.ph_mean_7d:.2f} ± {stab.ph_std_7d:.3f}"
            ph_st = (
                HealthStatus.SAFE
                if (stab.ph_std_7d or 0) < 0.3
                else HealthStatus.WARNING
            )
            ph_t = (
                f"14d: {stab.ph_mean_14d:.2f} ± {stab.ph_std_14d:.3f}"
                if stab.ph_mean_14d is not None
                else "—"
            )
        else:
            ph_v, ph_st, ph_t = "—", HealthStatus.SAFE, "—"
        self._set_card(self.ph_stab_card, ph_v, ph_t, ph_st)

        # Temperature
        if stab.temp_mean_7d is not None:
            t_v = f"{stab.temp_mean_7d:.1f} ± {stab.temp_std_7d:.2f}°C"
            t_st = (
                HealthStatus.SAFE
                if (stab.temp_std_7d or 0) < 1.0
                else HealthStatus.WARNING
            )
            t_t = (
                f"14d: {stab.temp_mean_14d:.1f} ± {stab.temp_std_14d:.2f}°C"
                if stab.temp_mean_14d is not None
                else "—"
            )
        else:
            t_v, t_st, t_t = "—", HealthStatus.SAFE, "—"
        self._set_card(self.temp_stab_card, t_v, t_t, t_st)
