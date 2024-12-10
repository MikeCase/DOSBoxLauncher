import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class DirectorySelectDialog(Gtk.Dialog):
    def __init__(self, parent, cfg_file_entry):
        super().__init__(title="Select Directory", transient_for=parent)
        
        # Create a file chooser dialog for selecting directories
        self.file_chooser = Gtk.FileChooserNative(
            title="Select a Directory",
            transient_for=parent,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        
        # Show the dialog
        self.file_chooser.set_modal(True)
        self.entry = cfg_file_entry
        
        # Run the dialog and handle the response
        self.file_chooser.connect('response', self.on_response)
        self.file_chooser.show()

    def on_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.ACCEPT:
            selected_folder = self.file_chooser.get_file().get_path()
            self.entry.set_text(selected_folder)
            # print(f"Selected directory: {selected_folder}")
        dialog.destroy()