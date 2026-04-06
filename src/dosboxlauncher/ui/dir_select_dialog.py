"""Directory select dialog."""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DirectorySelectDialog(Gtk.Dialog):
    """Dialog for selecting a directory."""

    def __init__(self, parent: Gtk.Window, target_entry: Gtk.Entry) -> None:
        super().__init__(title="Select Directory", transient_for=parent, flags=0)

        self.target_entry = target_entry
        self.file_chooser = Gtk.FileChooserNative(
            title="Select a Directory",
            transient_for=parent,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        self.file_chooser.set_modal(True)
        self.file_chooser.connect("response", self._on_response)
        self.file_chooser.show()

    def _on_response(self, dialog: Gtk.Dialog, response_id: int) -> None:
        """Handle dialog response."""
        if response_id == Gtk.ResponseType.ACCEPT:
            path = self.file_chooser.get_file().get_path()
            self.target_entry.set_text(path)
        dialog.destroy()
