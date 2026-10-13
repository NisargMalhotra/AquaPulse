"""
AquaPulse – My Aquarium View
=============================
Setup screen for tank profile: aquarium name, size (litres/gallons),
fish species selection, and species-specific parameter recommendations.
"""

from typing import Optional

import customtkinter as ctk
from tkinter import messagebox

from models.database import DatabaseManager
from utils.constants import Colors
from utils.fish_data import FISH_PROFILES, FISH_SPECIES_LIST


class AquariumView(ctk.CTkFrame):
    """Aquarium profile setup and species information panel."""

    def __init__(self, parent: ctk.CTkFrame, db: DatabaseManager) -> None:
        super().__init__(parent, fg_color=Colors.BG_DARK)
        self.db = db
        self._build_ui()

    # ─── UI Construction ─────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """Build the profile setup layout."""
        # ── Header ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(28, 8))

        ctk.CTkLabel(
            header,
            text="🐟 My Aquarium",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=Colors.TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Set up your tank profile for species-specific thresholds and recommendations.",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_SECONDARY,
        ).pack(anchor="w", pady=(4, 0))

        # ── Scrollable body ─────────────────────────────────────────
        body = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=Colors.BG_TERTIARY,
        )
        body.pack(fill="both", expand=True, padx=32, pady=12)

        # ── Card: Tank Details ──────────────────────────────────────
        tank_card = self._card(body, "🏠 Tank Details")

        ctk.CTkLabel(
            tank_card, text="Aquarium Name",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_SECONDARY,
        ).grid(row=1, column=0, padx=(16, 8), pady=6, sticky="w")

        self.name_var = ctk.StringVar(value="My Aquarium")
        ctk.CTkEntry(
            tank_card, textvariable=self.name_var, width=250,
            font=ctk.CTkFont(size=13),
            fg_color=Colors.BG_DARK,
            text_color=Colors.TEXT_PRIMARY,
            border_width=1, border_color=Colors.BORDER, corner_radius=8,
        ).grid(row=1, column=1, padx=(0, 16), pady=6, sticky="e")

        ctk.CTkLabel(
            tank_card, text="Tank Size (litres)",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_SECONDARY,
        ).grid(row=2, column=0, padx=(16, 8), pady=6, sticky="w")

        self.size_var = ctk.StringVar(value="19.0")
        ctk.CTkEntry(
            tank_card, textvariable=self.size_var, width=250,
            font=ctk.CTkFont(size=13),
            fg_color=Colors.BG_DARK,
            text_color=Colors.TEXT_PRIMARY,
            border_width=1, border_color=Colors.BORDER, corner_radius=8,
        ).grid(row=2, column=1, padx=(0, 16), pady=6, sticky="e")

        # Gallons helper label
        self.gallons_label = ctk.CTkLabel(
            tank_card, text="≈ 5.0 gallons",
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_MUTED,
        )
        self.gallons_label.grid(row=3, column=1, padx=(0, 16), sticky="e")
        self.size_var.trace_add("write", self._update_gallons)

        tank_card.grid_columnconfigure(1, weight=1)

        # ── Card: Fish Species ──────────────────────────────────────
        species_card = self._card(body, "🐠 Fish Species")

        ctk.CTkLabel(
            species_card, text="Select your primary fish",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_SECONDARY,
        ).grid(row=1, column=0, padx=(16, 8), pady=6, sticky="w")

        display_names = [name for _, name in FISH_SPECIES_LIST]
        self.species_var = ctk.StringVar(value=display_names[0])
        self.species_menu = ctk.CTkOptionMenu(
            species_card,
            values=display_names,
            variable=self.species_var,
            width=250,
            font=ctk.CTkFont(size=13),
            fg_color=Colors.BG_DARK,
            button_color=Colors.ACCENT_BLUE,
            button_hover_color=Colors.ACCENT_CYAN,
            text_color=Colors.TEXT_PRIMARY,
            dropdown_fg_color=Colors.BG_SECONDARY,
            dropdown_text_color=Colors.TEXT_PRIMARY,
            dropdown_hover_color=Colors.BG_TERTIARY,
            command=self._on_species_change,
        )
        self.species_menu.grid(row=1, column=1, padx=(0, 16), pady=6, sticky="e")
        species_card.grid_columnconfigure(1, weight=1)

        # ── Save Button ─────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(body, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(8, 16))

        ctk.CTkButton(
            btn_frame,
            text="💾  Save Profile",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=48, corner_radius=10,
            fg_color=Colors.ACCENT_CYAN,
            hover_color=Colors.ACCENT_BLUE,
            text_color=Colors.BG_DARK,
            command=self._save_profile,
        ).pack(ipadx=24)

        self.status_label = ctk.CTkLabel(
            btn_frame, text="",
            font=ctk.CTkFont(size=12),
            text_color=Colors.SAFE_GREEN,
        )
        self.status_label.pack(pady=(4, 0))

        # ── Card: Species Info (dynamic) ────────────────────────────
        self.info_card = self._card(body, "📋 Species Information")
        self.info_content = ctk.CTkFrame(
            self.info_card, fg_color="transparent",
        )
        self.info_content.grid(
            row=1, column=0, columnspan=2,
            padx=16, pady=(4, 12), sticky="we",
        )
        self.info_card.grid_columnconfigure(0, weight=1)

        # ── Card: Ideal Parameters (dynamic) ────────────────────────
        self.params_card = self._card(body, "🌡️ Ideal Water Parameters")
        self.params_content = ctk.CTkFrame(
            self.params_card, fg_color="transparent",
        )
        self.params_content.grid(
            row=1, column=0, columnspan=2,
            padx=16, pady=(4, 12), sticky="we",
        )
        self.params_card.grid_columnconfigure(0, weight=1)

        # Load saved profile or show defaults
        self._load_profile()
        self._on_species_change(self.species_var.get())

    # ─── Helpers ─────────────────────────────────────────────────────────

    def _card(self, parent: ctk.CTkFrame, title: str) -> ctk.CTkFrame:
        """Styled card with a title row."""
        card = ctk.CTkFrame(
            parent,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=12,
            border_width=1,
            border_color=Colors.BORDER,
        )
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Colors.ACCENT_BLUE,
        ).grid(row=0, column=0, columnspan=2, padx=16, pady=(12, 4), sticky="w")
        card.grid_columnconfigure(1, weight=1)
        return card

    def _get_species_key(self) -> str:
        """Map the display name back to the profile key."""
        display = self.species_var.get()
        for key, name in FISH_SPECIES_LIST:
            if name == display:
                return key
        return "betta"

    def _update_gallons(self, *_args: object) -> None:
        """Update the gallons helper when litres changes."""
        try:
            litres = float(self.size_var.get())
            gallons = litres / 3.785
            self.gallons_label.configure(text=f"≈ {gallons:.1f} gallons")
        except ValueError:
            self.gallons_label.configure(text="")

    # ─── Species Change ──────────────────────────────────────────────────

    def _on_species_change(self, _display_name: str) -> None:
        """Update info and params cards when the species dropdown changes."""
        key = self._get_species_key()
        profile = FISH_PROFILES.get(key)
        if not profile:
            return

        # ── Clear previous content ──────────────────────────────────
        for widget in self.info_content.winfo_children():
            widget.destroy()
        for widget in self.params_content.winfo_children():
            widget.destroy()

        # ── Species Info ────────────────────────────────────────────
        info_rows = [
            ("Scientific Name", profile["scientific_name"]),
            ("Care Level", profile["care_level"]),
            ("Temperament", profile["temperament"]),
            ("Lifespan", f"{profile['lifespan_years']} years"),
            ("Minimum Tank Size", f"{profile['min_tank_liters']} litres ({profile['min_tank_liters']/3.785:.0f} gal)"),
            ("Diet", profile["diet"]),
        ]
        for i, (label, value) in enumerate(info_rows):
            ctk.CTkLabel(
                self.info_content, text=label,
                font=ctk.CTkFont(size=12),
                text_color=Colors.TEXT_MUTED,
            ).grid(row=i, column=0, padx=(0, 12), pady=2, sticky="w")
            ctk.CTkLabel(
                self.info_content, text=value,
                font=ctk.CTkFont(size=12),
                text_color=Colors.TEXT_PRIMARY,
            ).grid(row=i, column=1, pady=2, sticky="w")

        # Notes
        ctk.CTkLabel(
            self.info_content,
            text=profile["notes"],
            font=ctk.CTkFont(size=11),
            text_color=Colors.WARNING_AMBER,
            wraplength=500,
            justify="left",
        ).grid(row=len(info_rows), column=0, columnspan=2, pady=(8, 0), sticky="w")

        # ── Ideal Parameters ────────────────────────────────────────
        thresholds = profile["thresholds"]
        param_display = [
            ("Ammonia (NH₃)", "ammonia_ppm", "ppm"),
            ("Nitrite (NO₂⁻)", "nitrite_ppm", "ppm"),
            ("Nitrate (NO₃⁻)", "nitrate_ppm", "ppm"),
            ("pH Level", "ph", ""),
            ("Temperature", "temperature_c", "°C"),
        ]
        for i, (label, key_name, unit) in enumerate(param_display):
            t = thresholds[key_name]
            if "safe_min" in t:
                safe_range = f"{t['safe_min']}–{t['safe_max']} {unit}"
                warn_range = f"{t.get('warning_min', '?')}–{t.get('warning_max', '?')} {unit}"
            else:
                safe_range = f"≤ {t['safe_max']} {unit}"
                warn_range = f"≤ {t['warning_max']} {unit}"

            ctk.CTkLabel(
                self.params_content, text=label,
                font=ctk.CTkFont(size=12),
                text_color=Colors.TEXT_MUTED,
            ).grid(row=i, column=0, padx=(0, 16), pady=3, sticky="w")
            ctk.CTkLabel(
                self.params_content, text=f"Safe: {safe_range}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=Colors.SAFE_GREEN,
            ).grid(row=i, column=1, padx=(0, 16), pady=3, sticky="w")
            ctk.CTkLabel(
                self.params_content, text=f"Warning: {warn_range}",
                font=ctk.CTkFont(size=12),
                text_color=Colors.WARNING_AMBER,
            ).grid(row=i, column=2, pady=3, sticky="w")

        # Tank size warning
        try:
            current_size = float(self.size_var.get())
            if current_size < profile["min_tank_liters"]:
                ctk.CTkLabel(
                    self.params_content,
                    text=(
                        f"⚠️  Your tank ({current_size:.0f} L) is below the recommended "
                        f"minimum of {profile['min_tank_liters']} L for {profile['name']}!"
                    ),
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=Colors.CRITICAL_RED,
                    wraplength=500,
                    justify="left",
                ).grid(
                    row=len(param_display), column=0, columnspan=3,
                    pady=(8, 0), sticky="w",
                )
        except ValueError:
            pass

    # ─── Persistence ─────────────────────────────────────────────────────

    def _load_profile(self) -> None:
        """Load the saved aquarium profile from the database."""
        try:
            profile = self.db.get_profile()
            if profile:
                self.name_var.set(profile.get("tank_name", "My Aquarium"))
                self.size_var.set(str(profile.get("tank_size_liters", 19.0)))
                species_key = profile.get("fish_species", "betta")
                for key, name in FISH_SPECIES_LIST:
                    if key == species_key:
                        self.species_var.set(name)
                        break
        except RuntimeError:
            pass  # no profile yet — use defaults

    def _save_profile(self) -> None:
        """Validate and save the aquarium profile."""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Validation Error", "Aquarium name cannot be empty.")
            return

        try:
            size = float(self.size_var.get())
            if size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Validation Error", "Tank size must be a positive number (litres)."
            )
            return

        species_key = self._get_species_key()

        try:
            self.db.save_profile(name, size, species_key)
            self.status_label.configure(
                text="✅ Profile saved successfully!",
                text_color=Colors.SAFE_GREEN,
            )
            # Refresh species info (in case tank size changed → warning)
            self._on_species_change(self.species_var.get())
        except RuntimeError as exc:
            messagebox.showerror("Database Error", str(exc))

    def on_show(self) -> None:
        """Reload profile data when tab is selected."""
        self._load_profile()
        self._on_species_change(self.species_var.get())

    def get_fish_species(self) -> str:
        """Return the currently selected fish species key."""
        return self._get_species_key()
