"""
AquaPulse – Main Application Window
====================================
Root ``CTk`` window with a fixed-width sidebar for navigation and a
right-side content area that swaps between six view frames:

1. 🐟 My Aquarium  – Tank profile and fish species setup
2. 📝 Log Data     – Data entry form
3. 📊 Dashboard    – Embedded analytical charts
4. 🔮 Predictions  – KPI cards and maintenance countdown
5. 🩺 Diagnosis    – AI-powered fish health diagnosis
6. 📋 History      – Searchable records table with CSV export

Handles:
* Sidebar button highlighting on tab switch.
* Calling ``on_show()`` on each frame when it becomes visible.
* Clean shutdown (database close + Matplotlib figure cleanup).
"""

from typing import Dict

import customtkinter as ctk

from controllers.analytics_engine import AnalyticsEngine
from models.database import DatabaseManager
from utils.constants import APP_NAME, APP_SUBTITLE, APP_VERSION, Colors
from views.aquarium_view import AquariumView
from views.dashboard_view import DashboardView
from views.diagnosis_view import DiagnosisView
from views.history_view import HistoryView
from views.log_data_view import LogDataView
from views.predictive_view import PredictiveView


class AquaPulseApp(ctk.CTk):
    """Top-level application window with sidebar navigation."""

    def __init__(self) -> None:
        super().__init__()

        # ── Window chrome ───────────────────────────────────────────
        self.title(f"{APP_NAME}  —  {APP_SUBTITLE}")
        self.geometry("1400x820")
        self.minsize(1100, 700)
        self.configure(fg_color=Colors.BG_DARK)

        # ── Shared services ─────────────────────────────────────────
        self.db = DatabaseManager()
        self.engine = AnalyticsEngine()

        # ── Grid layout: sidebar (col 0) + content (col 1) ─────────
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content()

        # Default tab
        self._show_frame("aquarium")

        # Clean shutdown on window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ─── Sidebar ─────────────────────────────────────────────────────────

    def _build_sidebar(self) -> None:
        """Construct the fixed-width navigation sidebar."""
        sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=Colors.BG_SECONDARY,
            border_width=1,
            border_color=Colors.BORDER,
        )
        sidebar.grid(row=0, column=0, sticky="nswe")
        sidebar.grid_propagate(False)
        sidebar.pack_propagate(False)

        # ── Branding ────────────────────────────────────────────────
        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=16, pady=(24, 4))

        ctk.CTkLabel(
            brand,
            text="🌊 AquaPulse",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=Colors.ACCENT_CYAN,
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand,
            text="Nitrogen Cycle Tracker",
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_SECONDARY,
        ).pack(anchor="w", pady=(2, 0))

        # Separator
        ctk.CTkFrame(
            sidebar, height=1, fg_color=Colors.BORDER,
        ).pack(fill="x", padx=16, pady=16)

        # ── Navigation buttons ──────────────────────────────────────
        nav = [
            ("🐟  My Aquarium", "aquarium"),
            ("📝  Log Data", "log"),
            ("📊  Dashboard", "dashboard"),
            ("🔮  Predictions", "predictive"),
            ("🩺  Diagnosis", "diagnosis"),
            ("📋  History", "history"),
        ]

        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        for label, key in nav:
            btn = ctk.CTkButton(
                sidebar,
                text=label,
                font=ctk.CTkFont(size=14),
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                text_color=Colors.TEXT_SECONDARY,
                hover_color=Colors.BG_TERTIARY,
                command=lambda k=key: self._show_frame(k),
            )
            btn.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[key] = btn

        # ── Version badge ───────────────────────────────────────────
        ctk.CTkLabel(
            sidebar,
            text=f"v{APP_VERSION}",
            font=ctk.CTkFont(size=10),
            text_color=Colors.TEXT_MUTED,
        ).pack(side="bottom", pady=12)

    # ─── Content Area ────────────────────────────────────────────────────

    def _build_content(self) -> None:
        """Instantiate all view frames inside a shared content area."""
        content = ctk.CTkFrame(
            self, fg_color=Colors.BG_DARK, corner_radius=0,
        )
        content.grid(row=0, column=1, sticky="nswe")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=1)

        self.frames: Dict[str, ctk.CTkFrame] = {
            "aquarium": AquariumView(content, self.db),
            "log": LogDataView(content, self.db),
            "dashboard": DashboardView(content, self.db, self.engine),
            "predictive": PredictiveView(content, self.db, self.engine),
            "diagnosis": DiagnosisView(content, self.db),
            "history": HistoryView(content, self.db),
        }

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nswe")

    # ─── Navigation ──────────────────────────────────────────────────────

    def _show_frame(self, key: str) -> None:
        """Raise *key*'s frame and update sidebar highlights."""
        for name, btn in self.nav_buttons.items():
            if name == key:
                btn.configure(
                    fg_color=Colors.BG_TERTIARY,
                    text_color=Colors.ACCENT_CYAN,
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=Colors.TEXT_SECONDARY,
                )

        frame = self.frames[key]
        frame.tkraise()

        # Let the frame refresh its data
        if hasattr(frame, "on_show"):
            frame.on_show()

    # ─── Shutdown ────────────────────────────────────────────────────────

    def _on_close(self) -> None:
        """Release resources and exit."""
        for frame in self.frames.values():
            if hasattr(frame, "cleanup"):
                frame.cleanup()
        self.db.close()
        self.destroy()
