import os
import subprocess
import gi
import json
from ConfigEditor.config_editor import ConfigEditor
from add_game_dialog import AddGameDialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk # type: ignore

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="DOSBox Launcher")

        # Load the UI from the .ui file
        builder = Gtk.Builder()
        try:
            builder.add_from_file("UI/dosboxfe-v2.ui")
        except Exception as e:
            print(f"Error loading UI: {e}")
            return

        # Get the main window from the builder
        self.hWind = builder.get_object("hWind")
        if not self.hWind:
            print("Error: Main window not found in UI file.")
            return

        # Show the window
        self.set_default_size(400,550)



        self.child = self.hWind.get_child()
        if self.child:
            self.hWind.remove(self.child)
            self.add(self.child)
        # self.add(hWind.get_child())

        # Get the widgets from the UI so they can be interacted with. 
        self.game_list = builder.get_object("game_list")
        self.add_game_btn = builder.get_object("addGameBtn")
        self.edit_config_btn = builder.get_object("edit_config_btn")
        self.launch_game_btn = builder.get_object("launch_game_btn")

        # Connect the signals so stuff happens.
        self.add_game_btn.connect("clicked", self.on_addGameBtn_clicked, self)
        self.edit_config_btn.connect("clicked", self.on_edit_config_btn_clicked, self)
        self.launch_game_btn.connect("clicked", self.on_launch_game)

        # Refresh the game list.
        self.refresh_game_list()


    def load_game_configs(self, json_file):
        """Load game configs from a JSON file."""
        with open(json_file, 'r') as f:
            return json.load(f)

    def refresh_game_list(self):
        # Clear existing rows
        for child in self.game_list.get_children():
            self.game_list.remove(child)

        # Load game configurations
        game_configs = self.load_game_configs("games.json")

        # Add new rows
        for config in game_configs:
            row = Gtk.ListBoxRow()
            label = Gtk.Label().new(config["name"])
            label.set_xalign(0)  # Align text to the start (left) if needed
            row.add(label)  # Use `add` in GTK+3 to pack widgets into a container
            row.show_all()  # Ensure the row and its children are visible
            row.config = config  # Store custom data directly on the row object
            self.game_list.add(row)  # Add the row to the ListBox


    def get_file_path(self, selected_row):
        """ Get file path of config """
        config_file_path = selected_row.config["config_file"]

        label = selected_row.get_child().get_text().replace(" ","").lower()
        config_file_name = f"{label}.conf"

        file_path = os.path.join(config_file_path, config_file_name)

        # check to see if the file path exists
        if os.path.exists(file_path):
            return file_path



    #############
    ## Signals ##
    #############

    def on_addGameBtn_clicked(self, btn, hWind):
        # Open the Add Game dialog when the button is clicked
        add_game_dialog = AddGameDialog(hWind)
        self.refresh_game_list()

    def on_edit_config_btn_clicked(self, btn, hWind):
        selected_row = self.game_list.get_selected_row()
        if selected_row:
            label = selected_row.get_child()
            print(f"Selected: {label.get_text()} - {selected_row.config['config_file']}")

            # Open the config editor window
            ConfigEditor(hWind, selected_row)
        else:
            print("Nothing selected.")

    def on_launch_game(self, btn):
        selected_row = self.game_list.get_selected_row()
        if selected_row:
            file_path = self.get_file_path(selected_row)
            label = selected_row.get_child().get_text()
            game_config = selected_row.config
            if game_config and "config_file" in game_config:
                print(f"Launching {label} with {file_path}")
                try:
                    subprocess.Popen(['dosbox', '-conf', file_path])
                except FileNotFoundError:
                    print("Error: DOSBox is not installed or not found in PATH")
            else:
                print(f"Error: {label} does not have a valid configuration file. \nUsing: {file_path}")
        else:
            print("Error: No game selected fool!")
