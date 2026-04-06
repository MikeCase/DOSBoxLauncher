"""DOSBox Launcher application entry point."""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DOSBoxLauncherApp(Gtk.Application):
    """Main application class."""

    def __init__(self) -> None:
        super().__init__(application_id="com.example.dosboxlauncher")

    def do_activate(self) -> None:
        if not hasattr(self, "window"):
            from .ui.main_window import MainWindow

            self.window = MainWindow(self)
            self.window.present()


def main() -> None:
    """Run the application."""
    app = DOSBoxLauncherApp()
    app.run()


if __name__ == "__main__":
    main()
