"""
AquaPulse – Fish Diagnosis View
================================
Chat-style interface where users describe symptoms in natural language
and receive ranked diagnoses with species-aware treatment plans,
medication dosages, and prevention tips.
"""

import customtkinter as ctk

from controllers.diagnosis_engine import DiagnosisEngine, DiagnosisResult
from models.database import DatabaseManager
from utils.constants import Colors
from utils.fish_data import FISH_SPECIES_LIST, QUICK_SYMPTOMS


class DiagnosisView(ctk.CTkFrame):
    """Chat-like fish health diagnosis panel."""

    def __init__(self, parent: ctk.CTkFrame, db: DatabaseManager) -> None:
        super().__init__(parent, fg_color=Colors.BG_DARK)
        self.db = db
        self.engine = DiagnosisEngine()
        self._build_ui()

    # ─── UI Construction ─────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """Build the diagnosis chat layout."""
        # ── Header ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(28, 8))

        ctk.CTkLabel(
            header,
            text="🩺 Fish Health Diagnosis",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=Colors.TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Describe your fish's symptoms and get instant treatment recommendations.",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_SECONDARY,
        ).pack(anchor="w", pady=(4, 0))

        # ── Species Selector ────────────────────────────────────────
        species_bar = ctk.CTkFrame(self, fg_color="transparent")
        species_bar.pack(fill="x", padx=32, pady=(8, 4))

        ctk.CTkLabel(
            species_bar,
            text="Diagnosing for:",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_SECONDARY,
        ).pack(side="left", padx=(0, 8))

        display_names = [name for _, name in FISH_SPECIES_LIST]
        self.species_var = ctk.StringVar(value=display_names[0])
        ctk.CTkOptionMenu(
            species_bar,
            values=display_names,
            variable=self.species_var,
            width=220,
            font=ctk.CTkFont(size=13),
            fg_color=Colors.BG_SECONDARY,
            button_color=Colors.ACCENT_BLUE,
            button_hover_color=Colors.ACCENT_CYAN,
            text_color=Colors.TEXT_PRIMARY,
            dropdown_fg_color=Colors.BG_SECONDARY,
            dropdown_text_color=Colors.TEXT_PRIMARY,
            dropdown_hover_color=Colors.BG_TERTIARY,
        ).pack(side="left")

        ctk.CTkButton(
            species_bar,
            text="🗑️ Clear Chat",
            width=100, height=32,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.CRITICAL_RED,
            text_color=Colors.TEXT_PRIMARY,
            command=self._clear_chat,
        ).pack(side="right")

        # ── Quick Symptom Buttons ───────────────────────────────────
        quick_frame = ctk.CTkFrame(self, fg_color="transparent")
        quick_frame.pack(fill="x", padx=32, pady=(8, 8))

        ctk.CTkLabel(
            quick_frame,
            text="Quick symptoms:",
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_MUTED,
        ).pack(side="left", padx=(0, 6))

        for symptom in QUICK_SYMPTOMS:
            ctk.CTkButton(
                quick_frame,
                text=symptom["label"],
                height=28,
                font=ctk.CTkFont(size=11),
                corner_radius=6,
                fg_color=Colors.BG_TERTIARY,
                hover_color=Colors.ACCENT_BLUE,
                text_color=Colors.TEXT_SECONDARY,
                command=lambda q=symptom["query"]: self._submit_query(q),
            ).pack(side="left", padx=2)

        # ── Chat Area (scrollable) ──────────────────────────────────
        self.chat_area = ctk.CTkScrollableFrame(
            self,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=12,
            border_width=1,
            border_color=Colors.BORDER,
            scrollbar_button_color=Colors.BG_TERTIARY,
        )
        self.chat_area.pack(
            fill="both", expand=True, padx=32, pady=(4, 8),
        )

        # Welcome message
        self._add_ai_welcome()

        # ── Input Bar ───────────────────────────────────────────────
        input_bar = ctk.CTkFrame(
            self,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=12,
            border_width=1,
            border_color=Colors.BORDER,
            height=56,
        )
        input_bar.pack(fill="x", padx=32, pady=(0, 20))
        input_bar.pack_propagate(False)

        self.input_var = ctk.StringVar()
        self.input_entry = ctk.CTkEntry(
            input_bar,
            textvariable=self.input_var,
            placeholder_text="Describe your fish's symptoms…  (e.g. 'my betta has white spots and is not eating')",
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            text_color=Colors.TEXT_PRIMARY,
            border_width=0,
        )
        self.input_entry.pack(
            side="left", fill="both", expand=True, padx=(16, 8), pady=8,
        )
        self.input_entry.bind("<Return>", lambda _: self._on_submit())

        ctk.CTkButton(
            input_bar,
            text="🔍 Diagnose",
            width=110, height=38,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8,
            fg_color=Colors.ACCENT_CYAN,
            hover_color=Colors.ACCENT_BLUE,
            text_color=Colors.BG_DARK,
            command=self._on_submit,
        ).pack(side="right", padx=(0, 8), pady=8)

    # ─── Chat Bubble Helpers ─────────────────────────────────────────────

    def _add_ai_welcome(self) -> None:
        """Display the initial AI welcome message."""
        welcome = ctk.CTkFrame(
            self.chat_area, fg_color=Colors.BG_TERTIARY, corner_radius=10,
        )
        welcome.pack(fill="x", padx=8, pady=8)

        ctk.CTkLabel(
            welcome,
            text="🩺 AquaPulse Diagnosis Assistant",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Colors.ACCENT_CYAN,
        ).pack(anchor="w", padx=14, pady=(12, 4))

        ctk.CTkLabel(
            welcome,
            text=(
                "Describe your fish's symptoms in plain English and I'll provide "
                "possible diagnoses with treatment recommendations.\n\n"
                "Examples:\n"
                "  •  \"My betta has fin rot and is losing its fins\"\n"
                "  •  \"White spots on my goldfish, scratching against rocks\"\n"
                "  •  \"Fish is floating sideways, not eating\"\n\n"
                "Tip: Select your fish species above for tailored advice!"
            ),
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_SECONDARY,
            wraplength=650,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 12))

    def _add_user_bubble(self, text: str) -> None:
        """Display a user message bubble."""
        bubble = ctk.CTkFrame(
            self.chat_area, fg_color=Colors.ACCENT_BLUE, corner_radius=10,
        )
        bubble.pack(anchor="e", padx=(80, 8), pady=(8, 2))

        ctk.CTkLabel(
            bubble,
            text=text,
            font=ctk.CTkFont(size=13),
            text_color=Colors.BG_DARK,
            wraplength=500,
            justify="left",
        ).pack(padx=14, pady=10)

    def _add_diagnosis_bubble(self, result: DiagnosisResult) -> None:
        """Render a full diagnosis card as an AI response bubble."""
        bubble = ctk.CTkFrame(
            self.chat_area, fg_color=Colors.BG_TERTIARY, corner_radius=10,
        )
        bubble.pack(fill="x", padx=8, pady=(2, 8))

        # ── Header: disease name + confidence ───────────────────────
        head = ctk.CTkFrame(bubble, fg_color="transparent")
        head.pack(fill="x", padx=14, pady=(12, 4))

        conf_color = {
            "Strong Match": Colors.SAFE_GREEN,
            "Good Match": Colors.WARNING_AMBER,
            "Possible Match": Colors.TEXT_MUTED,
        }.get(result.confidence, Colors.TEXT_MUTED)

        ctk.CTkLabel(
            head,
            text=f"{result.emoji} {result.disease_name}",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=Colors.TEXT_PRIMARY,
        ).pack(side="left")

        ctk.CTkLabel(
            head,
            text=f"  {result.confidence}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=conf_color,
        ).pack(side="left")

        ctk.CTkLabel(
            head,
            text=f"Severity: {result.severity}",
            font=ctk.CTkFont(size=11),
            text_color=Colors.WARNING_AMBER,
        ).pack(side="right")

        # ── Description ─────────────────────────────────────────────
        ctk.CTkLabel(
            bubble,
            text=result.description,
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_SECONDARY,
            wraplength=650,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 8))

        # ── Matched Symptoms ────────────────────────────────────────
        if result.matched_keywords:
            ctk.CTkLabel(
                bubble,
                text=f"🔍 Matched: {', '.join(result.matched_keywords)}",
                font=ctk.CTkFont(size=11),
                text_color=Colors.ACCENT_PURPLE,
                wraplength=650,
                justify="left",
            ).pack(anchor="w", padx=14, pady=(0, 8))

        # ── Species-Specific Advice ─────────────────────────────────
        if result.species_advice:
            advice_frame = ctk.CTkFrame(
                bubble, fg_color=Colors.BG_SECONDARY, corner_radius=8,
            )
            advice_frame.pack(fill="x", padx=14, pady=(0, 8))

            ctk.CTkLabel(
                advice_frame,
                text="🐠 Species-Specific Advice",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=Colors.ACCENT_CYAN,
            ).pack(anchor="w", padx=10, pady=(8, 2))

            ctk.CTkLabel(
                advice_frame,
                text=result.species_advice,
                font=ctk.CTkFont(size=12),
                text_color=Colors.TEXT_PRIMARY,
                wraplength=620,
                justify="left",
            ).pack(anchor="w", padx=10, pady=(0, 8))

        # ── Treatment Steps ─────────────────────────────────────────
        ctk.CTkLabel(
            bubble,
            text="💊 Treatment Plan",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=Colors.SAFE_GREEN,
        ).pack(anchor="w", padx=14, pady=(0, 2))

        treatment_text = "\n".join(result.treatment_steps)
        ctk.CTkLabel(
            bubble,
            text=treatment_text,
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_PRIMARY,
            wraplength=650,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 8))

        # ── Medications ─────────────────────────────────────────────
        if result.medications:
            ctk.CTkLabel(
                bubble,
                text="🧴 Medications",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=Colors.ACCENT_BLUE,
            ).pack(anchor="w", padx=14, pady=(0, 2))

            for med in result.medications:
                med_line = f"  •  {med.name}:  {med.dosage}  ({med.notes})"
                ctk.CTkLabel(
                    bubble,
                    text=med_line,
                    font=ctk.CTkFont(size=12),
                    text_color=Colors.TEXT_PRIMARY,
                    wraplength=630,
                    justify="left",
                ).pack(anchor="w", padx=14, pady=1)

        # ── Prevention ──────────────────────────────────────────────
        if result.prevention:
            ctk.CTkLabel(
                bubble,
                text="🛡️ Prevention",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=Colors.TEXT_MUTED,
            ).pack(anchor="w", padx=14, pady=(8, 2))

            for tip in result.prevention:
                ctk.CTkLabel(
                    bubble,
                    text=f"  •  {tip}",
                    font=ctk.CTkFont(size=11),
                    text_color=Colors.TEXT_MUTED,
                    wraplength=630,
                    justify="left",
                ).pack(anchor="w", padx=14, pady=1)

        # Bottom padding
        ctk.CTkFrame(bubble, fg_color="transparent", height=8).pack()

    def _add_no_match_bubble(self) -> None:
        """Display when no diseases match the symptoms."""
        bubble = ctk.CTkFrame(
            self.chat_area, fg_color=Colors.BG_TERTIARY, corner_radius=10,
        )
        bubble.pack(fill="x", padx=8, pady=(2, 8))

        ctk.CTkLabel(
            bubble,
            text="🤔 No matching conditions found",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Colors.WARNING_AMBER,
        ).pack(anchor="w", padx=14, pady=(12, 4))

        ctk.CTkLabel(
            bubble,
            text=(
                "I couldn't match your description to a known condition. Try:\n\n"
                "  •  Using different words to describe the symptoms\n"
                "  •  Clicking one of the quick symptom buttons above\n"
                "  •  Describing physical changes (spots, swelling, color changes)\n"
                "  •  Mentioning behavioral changes (not eating, floating, hiding)\n\n"
                "If symptoms persist, please consult a veterinarian who specialises in fish."
            ),
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_SECONDARY,
            wraplength=650,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 12))

    # ─── Submission Logic ────────────────────────────────────────────────

    def _get_species_key(self) -> str:
        """Map display name to species key."""
        display = self.species_var.get()
        for key, name in FISH_SPECIES_LIST:
            if name == display:
                return key
        return "betta"

    def _submit_query(self, query: str) -> None:
        """Run diagnosis on a given query string."""
        self.input_var.set("")
        self._add_user_bubble(query)

        species = self._get_species_key()
        results = self.engine.diagnose(query, fish_species=species, max_results=3)

        if results:
            for result in results:
                self._add_diagnosis_bubble(result)
        else:
            self._add_no_match_bubble()

        # Scroll to bottom
        self.chat_area._parent_canvas.yview_moveto(1.0)

    def _on_submit(self) -> None:
        """Handle the user pressing Enter or clicking Diagnose."""
        query = self.input_var.get().strip()
        if not query:
            return
        self._submit_query(query)

    def _clear_chat(self) -> None:
        """Remove all chat messages and show the welcome again."""
        for widget in self.chat_area.winfo_children():
            widget.destroy()
        self._add_ai_welcome()

    def on_show(self) -> None:
        """Sync the species selector with the saved profile."""
        try:
            profile = self.db.get_profile()
            if profile:
                species_key = profile.get("fish_species", "betta")
                for key, name in FISH_SPECIES_LIST:
                    if key == species_key:
                        self.species_var.set(name)
                        break
        except RuntimeError:
            pass
