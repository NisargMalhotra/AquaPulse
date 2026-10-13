"""
AquaPulse – Dashboard View
==========================
Embedded dark-themed Matplotlib / Seaborn charts for:

1. **Nitrogen Cycle Progression** – NH₃, NO₂⁻, NO₃⁻ trends over time
   with safety-threshold markers and water-change event lines.
2. **Parameter Stability** – pH and Temperature rolling means ± σ bands
   with safe-zone shading.

All :class:`Figure` references are tracked and explicitly closed before
each redraw to prevent Matplotlib memory leaks.
"""

import matplotlib
matplotlib.use("Agg")  # must be set before any pyplot import

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import Optional

import customtkinter as ctk
import pandas as pd

from controllers.analytics_engine import AnalyticsEngine
from models.database import DatabaseManager
from utils.constants import CHART_STYLE, Colors, THRESHOLDS


class DashboardView(ctk.CTkFrame):
    """Live dashboard with two embedded analytical charts."""

    def __init__(
        self,
        parent: ctk.CTkFrame,
        db: DatabaseManager,
        engine: AnalyticsEngine,
    ) -> None:
        super().__init__(parent, fg_color=Colors.BG_DARK)
        self.db = db
        self.engine = engine

        # Tracked Matplotlib objects for safe cleanup
        self._fig1: Optional[Figure] = None
        self._canvas1: Optional[FigureCanvasTkAgg] = None
        self._fig2: Optional[Figure] = None
        self._canvas2: Optional[FigureCanvasTkAgg] = None

        self._build_ui()

    # ─── UI Construction ─────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """Lay out the header, refresh button, and chart containers."""
        # ── Header bar ──────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(28, 8))

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.pack(fill="x")

        ctk.CTkLabel(
            title_row,
            text="📊 Live Dashboard & Analytics",
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
            command=self._refresh_charts,
        ).pack(side="right")

        ctk.CTkLabel(
            header,
            text="Nitrogen cycle progression and environmental stability trends.",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_SECONDARY,
        ).pack(anchor="w", pady=(4, 0))

        # ── Scrollable chart area ───────────────────────────────────
        self.chart_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=Colors.BG_TERTIARY,
        )
        self.chart_scroll.pack(fill="both", expand=True, padx=32, pady=12)

        # ── Chart 1: Nitrogen Cycle ─────────────────────────────────
        self.chart1_frame = self._chart_card(
            self.chart_scroll, "🔬 Nitrogen Cycle Progression"
        )
        self.chart1_container = ctk.CTkFrame(
            self.chart1_frame, fg_color="transparent",
        )
        self.chart1_container.pack(fill="x", padx=8, pady=(0, 8))

        # ── Chart 2: Stability ──────────────────────────────────────
        self.chart2_frame = self._chart_card(
            self.chart_scroll, "🌡️ Parameter Stability (Rolling Trends)"
        )
        self.chart2_container = ctk.CTkFrame(
            self.chart2_frame, fg_color="transparent",
        )
        self.chart2_container.pack(fill="x", padx=8, pady=(0, 8))

        # ── Empty-state label (hidden until needed) ─────────────────
        self.empty_label = ctk.CTkLabel(
            self.chart_scroll,
            text="No data yet — log some readings to see your charts!",
            font=ctk.CTkFont(size=14),
            text_color=Colors.TEXT_MUTED,
        )

    @staticmethod
    def _chart_card(parent: ctk.CTkFrame, title: str) -> ctk.CTkFrame:
        """Return a bordered card frame with a bold title."""
        card = ctk.CTkFrame(
            parent,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=12,
            border_width=1,
            border_color=Colors.BORDER,
        )
        card.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            card,
            text=f"  {title}",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=Colors.ACCENT_BLUE,
        ).pack(anchor="w", padx=12, pady=(12, 4))

        return card

    # ─── Refresh Logic ───────────────────────────────────────────────────

    def on_show(self) -> None:
        """Called each time this tab is raised."""
        self._refresh_charts()

    def _refresh_charts(self) -> None:
        """Reload data from the database and redraw both charts."""
        try:
            df = self.db.get_readings_as_dataframe()
        except RuntimeError:
            df = pd.DataFrame()

        if df.empty:
            self.empty_label.pack(pady=40)
            self._clear_chart(1)
            self._clear_chart(2)
            return

        self.empty_label.pack_forget()
        self._draw_nitrogen_chart(df)
        self._draw_stability_chart(df)

    # ─── Figure Lifecycle ────────────────────────────────────────────────

    def _clear_chart(self, chart_num: int) -> None:
        """Destroy existing canvas and close its Figure to free memory."""
        canvas: Optional[FigureCanvasTkAgg] = getattr(
            self, f"_canvas{chart_num}", None
        )
        fig: Optional[Figure] = getattr(self, f"_fig{chart_num}", None)

        if canvas is not None:
            canvas.get_tk_widget().destroy()
            setattr(self, f"_canvas{chart_num}", None)
        if fig is not None:
            plt.close(fig)
            setattr(self, f"_fig{chart_num}", None)

    def cleanup(self) -> None:
        """Release all Matplotlib resources (called on app shutdown)."""
        self._clear_chart(1)
        self._clear_chart(2)

    # ─── Chart 1: Nitrogen Cycle ─────────────────────────────────────────

    def _draw_nitrogen_chart(self, df: pd.DataFrame) -> None:
        """Render NH₃ / NO₂⁻ / NO₃⁻ trend lines with threshold markers."""
        self._clear_chart(1)

        with plt.rc_context(CHART_STYLE):
            fig, ax = plt.subplots(figsize=(10, 3.8), dpi=100)
            fig.patch.set_facecolor(Colors.BG_SECONDARY)

            ts = pd.to_datetime(df["timestamp"])

            # ── Series ──────────────────────────────────────────────
            ax.plot(
                ts, df["ammonia_ppm"],
                color=Colors.AMMONIA_COLOR, linewidth=2,
                marker="o", markersize=4, label="Ammonia (NH₃)",
            )
            ax.plot(
                ts, df["nitrite_ppm"],
                color=Colors.NITRITE_COLOR, linewidth=2,
                marker="s", markersize=4, label="Nitrite (NO₂⁻)",
            )
            ax.plot(
                ts, df["nitrate_ppm"],
                color=Colors.NITRATE_COLOR, linewidth=2,
                marker="^", markersize=4, label="Nitrate (NO₃⁻)",
            )

            # ── Threshold lines ─────────────────────────────────────
            ax.axhline(
                y=THRESHOLDS["ammonia_ppm"]["warning_max"],
                color=Colors.AMMONIA_COLOR,
                linestyle="--", alpha=0.4, linewidth=1,
                label="NH₃ Critical (0.25 ppm)",
            )
            ax.axhline(
                y=THRESHOLDS["nitrate_ppm"]["safe_max"],
                color=Colors.NITRATE_COLOR,
                linestyle="--", alpha=0.4, linewidth=1,
                label="NO₃⁻ Warning (20 ppm)",
            )

            # ── Water-change event markers ──────────────────────────
            wc_mask = df["water_changed"] == 1
            if wc_mask.any():
                for t in ts[wc_mask]:
                    ax.axvline(
                        x=t,
                        color=Colors.ACCENT_CYAN,
                        linestyle=":",
                        alpha=0.35,
                        linewidth=1,
                    )
                # single legend entry for all WC lines
                ax.axvline(
                    x=ts[wc_mask].iloc[0],
                    color=Colors.ACCENT_CYAN,
                    linestyle=":",
                    alpha=0,
                    label="Water Change",
                )

            ax.set_ylabel("Concentration (ppm)")
            ax.legend(loc="upper left", fontsize=8, framealpha=0.85)
            ax.grid(True, alpha=0.3)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
            fig.autofmt_xdate(rotation=30)
            fig.tight_layout(pad=1.5)

            self._fig1 = fig
            self._canvas1 = FigureCanvasTkAgg(fig, master=self.chart1_container)
            self._canvas1.draw()
            self._canvas1.get_tk_widget().pack(fill="x", expand=True)

    # ─── Chart 2: Stability ─────────────────────────────────────────────

    def _draw_stability_chart(self, df: pd.DataFrame) -> None:
        """Render pH and Temperature with 7-day rolling mean ± σ bands."""
        self._clear_chart(2)

        rolling_df = self.engine.get_rolling_dataframe(df, window=7)

        with plt.rc_context(CHART_STYLE):
            fig, (ax_ph, ax_temp) = plt.subplots(
                1, 2, figsize=(10, 3.8), dpi=100,
            )
            fig.patch.set_facecolor(Colors.BG_SECONDARY)

            ts = pd.to_datetime(rolling_df["timestamp"])

            # ── pH subplot ──────────────────────────────────────────
            ax_ph.plot(
                ts, rolling_df["ph"],
                color=Colors.PH_COLOR, alpha=0.35, linewidth=1,
                label="pH (raw)",
            )
            if "ph_rolling_mean_7d" in rolling_df.columns:
                mean = rolling_df["ph_rolling_mean_7d"]
                std = rolling_df["ph_rolling_std_7d"].fillna(0)
                ax_ph.plot(
                    ts, mean,
                    color=Colors.PH_COLOR, linewidth=2,
                    label="pH (7-day avg)",
                )
                ax_ph.fill_between(
                    ts, mean - std, mean + std,
                    color=Colors.PH_COLOR, alpha=0.15,
                )

            ax_ph.axhspan(
                THRESHOLDS["ph"]["safe_min"],
                THRESHOLDS["ph"]["safe_max"],
                color=Colors.SAFE_GREEN, alpha=0.07,
                label="Ideal range",
            )
            ax_ph.set_ylabel("pH")
            ax_ph.set_title("pH Stability", fontsize=12)
            ax_ph.legend(fontsize=8, loc="upper right")
            ax_ph.grid(True, alpha=0.3)
            ax_ph.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

            # ── Temperature subplot ─────────────────────────────────
            ax_temp.plot(
                ts, rolling_df["temperature_c"],
                color=Colors.TEMP_COLOR, alpha=0.35, linewidth=1,
                label="Temp (raw)",
            )
            if "temp_rolling_mean_7d" in rolling_df.columns:
                mean = rolling_df["temp_rolling_mean_7d"]
                std = rolling_df["temp_rolling_std_7d"].fillna(0)
                ax_temp.plot(
                    ts, mean,
                    color=Colors.TEMP_COLOR, linewidth=2,
                    label="Temp (7-day avg)",
                )
                ax_temp.fill_between(
                    ts, mean - std, mean + std,
                    color=Colors.TEMP_COLOR, alpha=0.15,
                )

            ax_temp.axhspan(
                THRESHOLDS["temperature_c"]["safe_min"],
                THRESHOLDS["temperature_c"]["safe_max"],
                color=Colors.SAFE_GREEN, alpha=0.07,
                label="Ideal range",
            )
            ax_temp.set_ylabel("Temperature (°C)")
            ax_temp.set_title("Temperature Stability", fontsize=12)
            ax_temp.legend(fontsize=8, loc="upper right")
            ax_temp.grid(True, alpha=0.3)
            ax_temp.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

            fig.autofmt_xdate(rotation=30)
            fig.tight_layout(pad=1.5)

            self._fig2 = fig
            self._canvas2 = FigureCanvasTkAgg(fig, master=self.chart2_container)
            self._canvas2.draw()
            self._canvas2.get_tk_widget().pack(fill="x", expand=True)
