import json
import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk # type: ignore

from dir_select_dialog import DirectorySelectDialog

class AddGameDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Add Game", transient_for=parent)
        
        # Load the add game dialog UI
        builder = Gtk.Builder()
        builder.add_from_file("UI/addgamedlg.ui")
        self.parent = parent
        # Get the dialog widget from the builder
        self.dialog = builder.get_object("add_game_dialog")
        # self.dialog.set_transient_for(parent)
        
        # Get the buttons and connect signals
        save_button = builder.get_object("save_button")
        cancel_button = builder.get_object("cancel_button")
        choose_path_btn = builder.get_object("choose_path_btn")
        
        save_button.connect("clicked", self.on_save_button_clicked, parent)
        cancel_button.connect("clicked", self.on_cancel_button_clicked)
        choose_path_btn.connect("clicked", self.on_path_choose_btn_clicked)
        
        self.game_name_entry = builder.get_object("game_name_entry")
        self.config_file_entry = builder.get_object("config_file_entry")

        self.dialog.show()

    def on_save_button_clicked(self, button, parent):
        game_name = self.game_name_entry.get_text()
        config_file = self.config_file_entry.get_text()

        if game_name and config_file:
            # Add the new game to the list (you can store this in a variable)
            new_game = {
                "name": game_name,
                "config_file": config_file
            }
            # For example, save to a JSON file or use in the main window.
            self.save_game_config(new_game)
            parent.refresh_game_list()
        self.dialog.destroy()

    def on_cancel_button_clicked(self, button):
        self.dialog.destroy()

    def save_game_config(self, new_game):
        # You could save the new game config to a JSON file or database here.
        json_file = "games.json"
        if os.path.exists(json_file):
            with open(json_file, "r") as f:
                game_configs = json.load(f)
        else:
            game_configs = []

        # Append the new game to the existing list
        game_configs.append(new_game)

        # Save the updated game list back to the JSON file
        with open(json_file, "w") as f:
            json.dump(game_configs, f, indent=4)

        print(f"Saved game config: {new_game}")
        self.destroy()

    def on_path_choose_btn_clicked(self, button):
        choose_dir_dialog = DirectorySelectDialog(self.dialog, self.config_file_entry)