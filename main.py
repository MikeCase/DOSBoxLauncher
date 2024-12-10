import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk # type: ignore
from main_window import MainWindow

# Define a class for the main application
class DOSBoxLauncherApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.dosboxoptions")

    def do_activate(self):
        if not hasattr(self, "window"):
            self.window = MainWindow(self)
            self.window.present()


# Run the application
if __name__ == "__main__":
    app = DOSBoxLauncherApp()
    app.run()
