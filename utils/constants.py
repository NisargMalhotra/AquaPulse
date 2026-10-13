"""
AquaPulse – Constants & Configuration
Centralized threshold definitions, color palettes, validation bounds,
and application-wide settings.
"""

from enum import Enum
from typing import Dict, Tuple


class HealthStatus(Enum):
    """Enumeration of water-health status levels."""

    SAFE = "Safe"
    WARNING = "Warning"
    CRITICAL = "Critical"


# ─── Safety Thresholds ──────────────────────────────────────────────────────────
# Based on established freshwater nano-aquarium guidelines.

THRESHOLDS: Dict[str, Dict[str, float]] = {
    "ammonia_ppm": {
        "safe_max": 0.1,       # ≤ 0.10 ppm → Safe
        "warning_max": 0.25,   # 0.10–0.25 ppm → Warning; > 0.25 → Critical
    },
    "nitrite_ppm": {
        "safe_max": 0.0,       # Ideally undetectable
        "warning_max": 0.5,    # Any detectable → Warning; > 0.50 → Critical
    },
    "nitrate_ppm": {
        "safe_max": 20.0,      # ≤ 20 ppm → Safe
        "warning_max": 40.0,   # 20–40 ppm → Warning; > 40 → Critical
    },
    "ph": {
        "safe_min": 6.5,
        "safe_max": 7.5,
        "warning_min": 6.0,
        "warning_max": 8.0,
    },
    "temperature_c": {
        "safe_min": 24.0,
        "safe_max": 28.0,
        "warning_min": 22.0,
        "warning_max": 30.0,
    },
}

# Default tap-water concentrations for dilution calculations
TAP_WATER_DEFAULTS: Dict[str, float] = {
    "ammonia_ppm": 0.0,
    "nitrite_ppm": 0.0,
    "nitrate_ppm": 5.0,   # Typical municipal tap water
}

# Target safe concentrations after a water change
TARGET_SAFE: Dict[str, float] = {
    "ammonia_ppm": 0.0,
    "nitrite_ppm": 0.0,
    "nitrate_ppm": 10.0,
}

# Nitrate threshold that triggers a mandatory water change
NITRATE_CHANGE_THRESHOLD: float = 20.0


# ─── UI Color Palette (Dark Theme) ──────────────────────────────────────────────

class Colors:
    """Dark-theme color constants for the AquaPulse UI and charts."""

    # Backgrounds
    BG_DARK: str = "#0d1117"
    BG_SECONDARY: str = "#161b22"
    BG_TERTIARY: str = "#21262d"
    BG_CARD: str = "#1c2128"

    # Accent
    ACCENT_BLUE: str = "#58a6ff"
    ACCENT_CYAN: str = "#39d2c0"
    ACCENT_PURPLE: str = "#bc8cff"

    # Status
    SAFE_GREEN: str = "#3fb950"
    WARNING_AMBER: str = "#d29922"
    CRITICAL_RED: str = "#f85149"

    # Text
    TEXT_PRIMARY: str = "#e6edf3"
    TEXT_SECONDARY: str = "#8b949e"
    TEXT_MUTED: str = "#484f58"

    # Borders
    BORDER: str = "#30363d"

    # Chart series
    AMMONIA_COLOR: str = "#f85149"
    NITRITE_COLOR: str = "#d29922"
    NITRATE_COLOR: str = "#58a6ff"
    PH_COLOR: str = "#bc8cff"
    TEMP_COLOR: str = "#39d2c0"


# ─── Matplotlib RC Overrides for Dark Charts ────────────────────────────────────

CHART_STYLE: Dict[str, object] = {
    "figure.facecolor": Colors.BG_DARK,
    "axes.facecolor": Colors.BG_SECONDARY,
    "axes.edgecolor": Colors.BORDER,
    "axes.labelcolor": Colors.TEXT_PRIMARY,
    "text.color": Colors.TEXT_PRIMARY,
    "xtick.color": Colors.TEXT_SECONDARY,
    "ytick.color": Colors.TEXT_SECONDARY,
    "grid.color": Colors.BG_TERTIARY,
    "grid.alpha": 0.6,
    "legend.facecolor": Colors.BG_TERTIARY,
    "legend.edgecolor": Colors.BORDER,
    "legend.labelcolor": Colors.TEXT_PRIMARY,
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
}


# ─── Validation Bounds ──────────────────────────────────────────────────────────

VALIDATION_RANGES: Dict[str, Tuple[float, float]] = {
    "ammonia_ppm": (0.0, 10.0),
    "nitrite_ppm": (0.0, 10.0),
    "nitrate_ppm": (0.0, 200.0),
    "ph": (0.0, 14.0),
    "temperature_c": (0.0, 45.0),
    "water_change_volume_pct": (0.0, 100.0),
}


# ─── Application Metadata ──────────────────────────────────────────────────────

APP_NAME: str = "AquaPulse"
APP_VERSION: str = "1.0.0"
APP_SUBTITLE: str = "Nano-Aquarium Nitrogen Cycle & Ecosystem Tracker"
DB_FILENAME: str = "aquapulse.db"
