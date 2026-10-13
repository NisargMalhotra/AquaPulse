"""
AquaPulse: Nano-Aquarium Nitrogen Cycle & Ecosystem Tracker
============================================================
Application entry point.

Usage::

    python main.py
"""

import customtkinter as ctk

from views.app import AquaPulseApp


def main() -> None:
    """Configure the theme and launch the main window."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = AquaPulseApp()
    app.mainloop()


if __name__ == "__main__":
    main()
