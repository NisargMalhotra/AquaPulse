"""
AquaPulse – Historical Records & Export View
=============================================
Searchable tabular display of all water-parameter readings backed by a
``ttk.Treeview`` styled for the dark theme.  Supports:

* Full-text search across notes and timestamps.
* Multi-row selection with bulk delete (confirmation dialog).
* CSV export of the complete dataset.
* CSV import with automatic table refresh.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Any, Dict, List

import customtkinter as ctk

from models.database import DatabaseManager
from utils.constants import Colors


class HistoryView(ctk.CTkFrame):
    """Searchable historical records table with CSV export/import."""

    def __init__(self, parent: ctk.CTkFrame, db: DatabaseManager) -> None:
        super().__init__(parent, fg_color=Colors.BG_DARK)
        self.db = db
        self._style_applied = False
        self._build_ui()

    # ─── UI Construction ─────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """Assemble header, toolbar, record count, and treeview."""
        # ── Header ──────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(28, 8))

        ctk.CTkLabel(
            header,
            text="📋 Historical Records",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=Colors.TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Browse, search, and export all logged water test data.",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_SECONDARY,
        ).pack(anchor="w", pady=(4, 0))

        # ── Toolbar ─────────────────────────────────────────────────
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=32, pady=(12, 8))

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            toolbar,
            textvariable=self.search_var,
            placeholder_text="🔍 Search notes or dates…",
            width=300,
            height=36,
            font=ctk.CTkFont(size=13),
            fg_color=Colors.BG_SECONDARY,
            text_color=Colors.TEXT_PRIMARY,
            border_width=1,
            border_color=Colors.BORDER,
            corner_radius=8,
        )
        search_entry.pack(side="left", padx=(0, 8))
        search_entry.bind("<Return>", lambda _e: self._search())

        ctk.CTkButton(
            toolbar,
            text="Search",
            width=80,
            height=36,
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            fg_color=Colors.ACCENT_BLUE,
            hover_color=Colors.ACCENT_CYAN,
            text_color=Colors.BG_DARK,
            command=self._search,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar,
            text="Show All",
            width=80,
            height=36,
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.ACCENT_BLUE,
            text_color=Colors.TEXT_PRIMARY,
            command=self._load_all,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar,
            text="☑ Select All",
            width=90,
            height=36,
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.ACCENT_BLUE,
            text_color=Colors.TEXT_PRIMARY,
            command=self._select_all,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            toolbar,
            text="☐ Deselect",
            width=90,
            height=36,
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.ACCENT_BLUE,
            text_color=Colors.TEXT_PRIMARY,
            command=self._deselect_all,
        ).pack(side="left", padx=(0, 16))

        # Right-side action buttons (packed right → left)
        ctk.CTkButton(
            toolbar,
            text="📥 Import CSV",
            width=120,
            height=36,
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.ACCENT_BLUE,
            text_color=Colors.TEXT_PRIMARY,
            command=self._import_csv,
        ).pack(side="right", padx=(4, 0))

        ctk.CTkButton(
            toolbar,
            text="📤 Export CSV",
            width=120,
            height=36,
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            fg_color=Colors.ACCENT_CYAN,
            hover_color=Colors.ACCENT_BLUE,
            text_color=Colors.BG_DARK,
            command=self._export_csv,
        ).pack(side="right", padx=(4, 0))

        ctk.CTkButton(
            toolbar,
            text="🗑️ Delete Selected",
            width=140,
            height=36,
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            fg_color=Colors.CRITICAL_RED,
            hover_color="#c93c37",
            text_color=Colors.TEXT_PRIMARY,
            command=self._delete_selected,
        ).pack(side="right", padx=(0, 4))

        # ── Record count ────────────────────────────────────────────
        self.count_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_MUTED,
        )
        self.count_label.pack(anchor="w", padx=32)

        # ── Treeview table ──────────────────────────────────────────
        table_frame = ctk.CTkFrame(
            self,
            fg_color=Colors.BG_SECONDARY,
            corner_radius=12,
            border_width=1,
            border_color=Colors.BORDER,
        )
        table_frame.pack(fill="both", expand=True, padx=32, pady=(8, 24))

        self._apply_treeview_style()

        columns = (
            "id", "timestamp", "ammonia", "nitrite",
            "nitrate", "ph", "temp", "wc", "wc_vol", "notes",
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="AquaPulse.Treeview",
            selectmode="extended",
        )

        headings: Dict[str, tuple[str, int]] = {
            "id": ("ID", 45),
            "timestamp": ("Timestamp", 155),
            "ammonia": ("NH₃ ppm", 80),
            "nitrite": ("NO₂⁻ ppm", 80),
            "nitrate": ("NO₃⁻ ppm", 80),
            "ph": ("pH", 60),
            "temp": ("Temp °C", 75),
            "wc": ("WC?", 50),
            "wc_vol": ("WC %", 55),
            "notes": ("Notes", 220),
        }

        for col, (heading, width) in headings.items():
            self.tree.heading(col, text=heading, anchor="center")
            anchor = "w" if col == "notes" else "center"
            self.tree.column(col, width=width, minwidth=40, anchor=anchor)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview,
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(
            side="left", fill="both", expand=True, padx=(8, 0), pady=8,
        )
        scrollbar.pack(side="right", fill="y", pady=8, padx=(0, 4))

    def _apply_treeview_style(self) -> None:
        """Apply a dark-theme style to ``ttk.Treeview`` (once)."""
        if self._style_applied:
            return
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "AquaPulse.Treeview",
            background=Colors.BG_SECONDARY,
            foreground=Colors.TEXT_PRIMARY,
            fieldbackground=Colors.BG_SECONDARY,
            borderwidth=0,
            font=("Segoe UI", 11),
            rowheight=28,
        )
        style.configure(
            "AquaPulse.Treeview.Heading",
            background=Colors.BG_TERTIARY,
            foreground=Colors.TEXT_PRIMARY,
            borderwidth=0,
            font=("Segoe UI", 11, "bold"),
        )
        style.map(
            "AquaPulse.Treeview",
            background=[("selected", Colors.BG_TERTIARY)],
            foreground=[("selected", Colors.ACCENT_CYAN)],
        )
        self._style_applied = True

    # ─── Data Operations ─────────────────────────────────────────────────

    def on_show(self) -> None:
        """Reload all data when the tab is selected."""
        self._load_all()

    def _populate(self, readings: List[Dict[str, Any]]) -> None:
        """Clear and repopulate the treeview with *readings*."""
        for child in self.tree.get_children():
            self.tree.delete(child)

        for r in readings:
            wc = r.get("water_changed", 0)
            self.tree.insert(
                "",
                "end",
                values=(
                    r["id"],
                    r["timestamp"],
                    f"{r['ammonia_ppm']:.2f}",
                    f"{r['nitrite_ppm']:.2f}",
                    f"{r['nitrate_ppm']:.2f}",
                    f"{r['ph']:.1f}",
                    f"{r['temperature_c']:.1f}",
                    "✓" if wc else "",
                    f"{r['water_change_volume_pct']:.0f}" if wc else "",
                    r.get("notes", ""),
                ),
            )

        self.count_label.configure(text=f"{len(readings)} record(s) found")

    def _load_all(self) -> None:
        """Fetch all readings and display them."""
        try:
            readings = self.db.get_all_readings()
            self._populate(readings)
            self.search_var.set("")
        except RuntimeError as exc:
            messagebox.showerror("Database Error", str(exc))

    def _search(self) -> None:
        """Filter displayed readings by the search query."""
        query = self.search_var.get().strip()
        if not query:
            self._load_all()
            return
        try:
            results = self.db.search_readings(query)
            self._populate(results)
        except RuntimeError as exc:
            messagebox.showerror("Search Error", str(exc))

    def _select_all(self) -> None:
        """Select every row in the treeview."""
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children)
            self.count_label.configure(
                text=f"{len(children)} record(s) selected",
            )

    def _deselect_all(self) -> None:
        """Clear the treeview selection."""
        self.tree.selection_remove(self.tree.selection())
        # Restore the regular count
        total = len(self.tree.get_children())
        self.count_label.configure(text=f"{total} record(s) found")

    def _delete_selected(self) -> None:
        """Delete selected rows after a confirmation dialog."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo(
                "No Selection", "Select one or more rows to delete."
            )
            return

        count = len(selected)
        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Permanently delete {count} reading(s)?",
        ):
            return

        try:
            for item in selected:
                vals = self.tree.item(item, "values")
                self.db.delete_reading(int(vals[0]))
            self._load_all()
        except (RuntimeError, ValueError) as exc:
            messagebox.showerror("Delete Error", str(exc))

    # ─── CSV Export / Import ─────────────────────────────────────────────

    def _export_csv(self) -> None:
        """Prompt for a save path and export all readings."""
        path = filedialog.asksaveasfilename(
            title="Export Readings to CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="aquapulse_export.csv",
        )
        if not path:
            return
        try:
            n = self.db.export_to_csv(path)
            messagebox.showinfo(
                "Export Complete",
                f"Exported {n} readings to:\n{path}",
            )
        except RuntimeError as exc:
            messagebox.showerror("Export Error", str(exc))

    def _import_csv(self) -> None:
        """Prompt for a CSV file and import its rows."""
        path = filedialog.askopenfilename(
            title="Import Readings from CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            n = self.db.import_from_csv(path)
            messagebox.showinfo("Import Complete", f"Imported {n} readings.")
            self._load_all()
        except RuntimeError as exc:
            messagebox.showerror("Import Error", str(exc))
