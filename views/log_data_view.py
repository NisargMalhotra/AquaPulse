"""
AquaPulse – Log Data View
=========================
Data-entry form with per-field validation, bounds checking,
and timestamp management for daily/weekly water test results.
"""

from datetime import datetime
from tkinter import messagebox
from typing import Optional

import customtkinter as ctk

from models.database import DatabaseManager
from utils.constants import Colors, VALIDATION_RANGES


class LogDataView(ctk.CTkFrame):
    """Water-test data-entry form with real-time input validation."""

    def __init__(self, parent: ctk.CTkFrame, db: DatabaseManager) -> None:
        super().__init__(parent, fg_color=Colors.BG_DARK)
        self.db = db
        self.wc_volume_entry: Optional[ctk.CTkEntry] = None
        self._build_ui()

    # ─── UI Construction ─────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """Assemble the full form layout."""
        # ── Header ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(28, 8))

        ctk.CTkLabel(
            header,
            text="📝 Log Water Test Results",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=Colors.TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Record your aquarium's daily or weekly chemical test readings.",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_SECONDARY,
        ).pack(anchor="w", pady=(4, 0))

        # ── Scrollable form body ────────────────────────────────────
        form = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=Colors.BG_TERTIARY,
        )
        form.pack(fill="both", expand=True, padx=32, pady=12)

        # ── Card: Nitrogen Parameters ───────────────────────────────
        n_card = self._card(form, "🧪 Nitrogen Cycle Parameters")
        self.ammonia_var = self._field(n_card, "Ammonia (ppm)", "0.0", row=0)
        self.nitrite_var = self._field(n_card, "Nitrite (ppm)", "0.0", row=1)
        self.nitrate_var = self._field(n_card, "Nitrate (ppm)", "0.0", row=2)

        # ── Card: Environmental ─────────────────────────────────────
        e_card = self._card(form, "🌡️ Environmental Parameters")
        self.ph_var = self._field(e_card, "pH Level", "7.0", row=0)
        self.temp_var = self._field(e_card, "Temperature (°C)", "26.0", row=1)

        # ── Card: Water Change ──────────────────────────────────────
        wc_card = self._card(form, "💧 Water Change")

        self.water_changed_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            wc_card,
            text="Water change performed today",
            variable=self.water_changed_var,
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_PRIMARY,
            fg_color=Colors.ACCENT_CYAN,
            hover_color=Colors.ACCENT_BLUE,
            command=self._toggle_wc_volume,
        ).grid(row=1, column=0, columnspan=2, padx=16, pady=(4, 4), sticky="w")

        self.wc_volume_var = self._field(
            wc_card, "Volume Changed (%)", "25.0", row=2,
        )
        # Disable until the checkbox is ticked
        if self.wc_volume_entry is not None:
            self.wc_volume_entry.configure(state="disabled")

        # ── Card: Notes ─────────────────────────────────────────────
        notes_card = self._card(form, "📓 Notes")
        self.notes_text = ctk.CTkTextbox(
            notes_card,
            height=80,
            font=ctk.CTkFont(size=13),
            fg_color=Colors.BG_DARK,
            text_color=Colors.TEXT_PRIMARY,
            border_width=1,
            border_color=Colors.BORDER,
            corner_radius=8,
        )
        self.notes_text.grid(
            row=1, column=0, columnspan=2, padx=16, pady=12, sticky="we",
        )
        notes_card.grid_columnconfigure(0, weight=1)

        # ── Card: Timestamp ─────────────────────────────────────────
        ts_card = self._card(form, "🕐 Timestamp")
        self.timestamp_var = self._field(
            ts_card,
            "Date & Time (YYYY-MM-DD HH:MM:SS)",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            row=0,
        )

        # ── Submit Button ───────────────────────────────────────────
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(16, 24))

        self.submit_btn = ctk.CTkButton(
            btn_frame,
            text="💾  Save Reading",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=48,
            corner_radius=10,
            fg_color=Colors.ACCENT_CYAN,
            hover_color=Colors.ACCENT_BLUE,
            text_color=Colors.BG_DARK,
            command=self._on_submit,
        )
        self.submit_btn.pack(pady=4, ipadx=24)

        self.status_label = ctk.CTkLabel(
            btn_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=Colors.SAFE_GREEN,
        )
        self.status_label.pack(pady=(4, 0))

    # ─── Widget Helpers ──────────────────────────────────────────────────

    def _card(self, parent: ctk.CTkFrame, title: str) -> ctk.CTkFrame:
        """Return a styled card section with a bold title row."""
        card = ctk.CTkFrame(
            parent,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=12,
            border_width=1,
            border_color=Colors.BORDER,
        )
        card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Colors.ACCENT_BLUE,
        ).grid(row=0, column=0, columnspan=2, padx=16, pady=(12, 4), sticky="w")

        card.grid_columnconfigure(1, weight=1)
        return card

    def _field(
        self,
        parent: ctk.CTkFrame,
        label: str,
        default: str,
        row: int,
    ) -> ctk.StringVar:
        """Add a *label + entry* row inside a card and return the StringVar."""
        grid_row = row + 1  # row 0 is the card title

        ctk.CTkLabel(
            parent,
            text=label,
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_SECONDARY,
        ).grid(row=grid_row, column=0, padx=(16, 8), pady=6, sticky="w")

        var = ctk.StringVar(value=default)
        entry = ctk.CTkEntry(
            parent,
            textvariable=var,
            width=220,
            font=ctk.CTkFont(size=13),
            fg_color=Colors.BG_DARK,
            text_color=Colors.TEXT_PRIMARY,
            border_width=1,
            border_color=Colors.BORDER,
            corner_radius=8,
        )
        entry.grid(row=grid_row, column=1, padx=(0, 16), pady=6, sticky="e")

        # Keep a reference to the volume entry for enable/disable toggling
        if "Volume" in label:
            self.wc_volume_entry = entry

        return var

    def _toggle_wc_volume(self) -> None:
        """Enable / disable the water-change volume field."""
        if self.wc_volume_entry is not None:
            state = "normal" if self.water_changed_var.get() else "disabled"
            self.wc_volume_entry.configure(state=state)

    # ─── Validation & Submission ─────────────────────────────────────────

    def _validate_float(self, raw: str, field_key: str) -> Optional[float]:
        """
        Parse *raw* as a float and bounds-check against
        :data:`VALIDATION_RANGES`.

        Returns the parsed value on success, or ``None`` after showing
        an error dialog.
        """
        try:
            val = float(raw.strip())
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                f"'{field_key}' must be a numeric value.\nGot: '{raw}'",
            )
            return None

        bounds = VALIDATION_RANGES.get(field_key)
        if bounds and not (bounds[0] <= val <= bounds[1]):
            messagebox.showerror(
                "Validation Error",
                f"'{field_key}' must be between {bounds[0]} and {bounds[1]}."
                f"\nGot: {val}",
            )
            return None

        return val

    def _on_submit(self) -> None:
        """Validate every field and persist a new reading to the database."""
        raw_fields = {
            "ammonia_ppm": self.ammonia_var.get(),
            "nitrite_ppm": self.nitrite_var.get(),
            "nitrate_ppm": self.nitrate_var.get(),
            "ph": self.ph_var.get(),
            "temperature_c": self.temp_var.get(),
        }

        validated: dict[str, float] = {}
        for key, raw in raw_fields.items():
            result = self._validate_float(raw, key)
            if result is None:
                return  # stop on first validation failure
            validated[key] = result

        # Water-change fields
        wc = self.water_changed_var.get()
        wc_vol = 0.0
        if wc:
            vol = self._validate_float(
                self.wc_volume_var.get(), "water_change_volume_pct"
            )
            if vol is None:
                return
            wc_vol = vol

        # Timestamp
        ts = self.timestamp_var.get().strip()
        try:
            datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Timestamp must follow YYYY-MM-DD HH:MM:SS format.",
            )
            return

        notes = self.notes_text.get("1.0", "end-1c").strip()

        # ── Persist ──────────────────────────────────────────────────
        try:
            self.db.insert_reading(
                ammonia_ppm=validated["ammonia_ppm"],
                nitrite_ppm=validated["nitrite_ppm"],
                nitrate_ppm=validated["nitrate_ppm"],
                ph=validated["ph"],
                temperature_c=validated["temperature_c"],
                water_changed=wc,
                water_change_volume_pct=wc_vol,
                notes=notes,
                timestamp=ts,
            )
            self.status_label.configure(
                text="✅ Reading saved successfully!",
                text_color=Colors.SAFE_GREEN,
            )
            self._reset_form()
        except RuntimeError as exc:
            messagebox.showerror("Database Error", str(exc))

    def _reset_form(self) -> None:
        """Reset all fields to their defaults."""
        self.ammonia_var.set("0.0")
        self.nitrite_var.set("0.0")
        self.nitrate_var.set("0.0")
        self.ph_var.set("7.0")
        self.temp_var.set("26.0")
        self.water_changed_var.set(False)
        self.wc_volume_var.set("25.0")
        self.notes_text.delete("1.0", "end")
        self.timestamp_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self._toggle_wc_volume()

    def on_show(self) -> None:
        """Refresh the timestamp default when the tab is re-selected."""
        self.timestamp_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
