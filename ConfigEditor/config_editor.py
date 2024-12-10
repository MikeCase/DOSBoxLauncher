# import configparser
import json
from ConfigEditor.dosbox_config_parser import DOSBoxConfigParser
from ConfigEditor.configfile_dataclasses import ComboBoxMappings, KEY_MAPPINGS, load_config
import os
from pprint import pprint
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk # type: ignore

class ConfigEditor(Gtk.Window):
    def __init__(self, parent, game = None):
        """ Main entry point for the ConfigEditor """
        super().__init__(title="DOSBox Config Editor", transient_for=parent)
        self.config = DOSBoxConfigParser()
        self.parent = parent
        # Load the editor UI
        builder = Gtk.Builder()
        builder.add_from_file("UI/config_options.ui")

        # Get the window object from the builder
        self.opts_window = builder.get_object("OptsWindow")

        self.game_opts = game
        self.load_game_config()
        # pprint(get_config_file_values(self.config))
        self.cfg_values = load_config(self.config)

        # Not yet sure if I want to map all the buffers.
        self.autoexec_buffer = builder.get_object("autoexec_tbuffer")
        self.serial1_buffer = builder.get_object("serial1_entry_buffer")
        self.serial2_buffer = builder.get_object("serial2_entry_buffer")
        self.serial3_buffer = builder.get_object("serial3_entry_buffer")
        self.serial4_buffer = builder.get_object("serial4_entry_buffer")


        # Trying to keep the widgets tidy since there's a lot of them. 
        # Should make it easier to use them in code as well. 
        self.sdl_widgets = {
            'fullscreen_sw': builder.get_object("fullscreen_sw"),
            "fulldouble_sw": builder.get_object("fulldouble_sw"),
            "full_resolution_cbox": builder.get_object("full_resolution_cbox"),
            "wind_res_cbox": builder.get_object("wind_res_cbox"),
            "output_cbox": builder.get_object("output_cbox"),
            "autolock_sw": builder.get_object("autolock_sw"),
            "sensitivity_spin": builder.get_object("sensitivity_spin"),
            "wait_on_error_sw": builder.get_object("wait_on_error_sw"),
            "priority_cbox": builder.get_object("priority_cbox"),
            "mapper_file_entry": builder.get_object("mapper_file_entry"),
            "use_scan_codes_sw": builder.get_object("use_scan_codes_sw"),
        }
        self.dosbox_widgets = {
            'language_entry': builder.get_object("language_entry"),
            'memsize_spin': builder.get_object('memsize_spin'),
            'machine_cbox': builder.get_object('machine_cbox'),
            'captures_entry': builder.get_object('captures_entry')
        }
        self.render_widgets = {
            'frameskip_spin': builder.get_object('frameskip_spin'),
            'aspect_sw': builder.get_object('aspect_sw'),
            'scaler_cbox': builder.get_object('scaler_cbox'),
        }
        self.cpu_widgets = {
            'core_cbox': builder.get_object('core_cbox'),
            'cpu_type_cbox': builder.get_object('cpu_type_cbox'),
            'cycles_cbox': builder.get_object('cycles_cbox'),
            'cycle_up_spin': builder.get_object('cycle_up_spin'),
            'cycle_down_spin': builder.get_object('cycle_down_spin'),
        }
        self.serial_widgets = {
            'serial1_cbox': builder.get_object('serial1_cbox'),
            'serial2_cbox': builder.get_object('serial2_cbox'),
            'serial3_cbox': builder.get_object('serial3_cbox'),
            'serial4_cbox': builder.get_object('serial4_cbox'),
        }
        self.dos_widgets = {
            'xms_sw': builder.get_object('xms_sw'),
            'ems_sw': builder.get_object('ems_sw'),
            'umb_sw': builder.get_object('umb_sw'),
            'keyboard_layout_cbox': builder.get_object('keyboard_layout_cbox'),
        }
        self.ipx_widgets = {
            'ipx_sw': builder.get_object('ipx_sw'),
        }
        self.autoexec_widgets = {
            'autoexec_tbox': builder.get_object('autoexec_tbox'),
        }
        self.widgets = {
            "sdl": self.sdl_widgets, 
            "dosbox": self.dosbox_widgets,
            "render": self.render_widgets,
            "cpu": self.cpu_widgets,
            "serial": self.serial_widgets,
            "dos": self.dos_widgets, 
            "ipx": self.ipx_widgets,
            "autoexec": self.autoexec_widgets,
        }

        save_btn = builder.get_object("save_config_btn")
        reload_btn = builder.get_object("reload_config_btn")
        cancel_btn = builder.get_object("cancel_btn")
        remove_config_btn = builder.get_object("remove_config_btn")

        save_btn.connect('clicked', self.save_config)
        reload_btn.connect('clicked', self.do_reload_config)
        cancel_btn.connect('clicked', self.close_window)
        remove_config_btn.connect('clicked', self.do_remove_config, parent)

        # Update all ui values with values from the config file.
        self.update_ui()

        self.opts_window.show()

    def close_window(self, hWnd):
        self.opts_window.destroy()

    def save_config(self, button=None):
        # Mapping of UI widget names to DOSBox config keys
        key_mapping = KEY_MAPPINGS

        # Iterate over each category of widgets
        for key, widget_group in self.widgets.items():
            for field, widget in widget_group.items():

                # Check if the field has a corresponding DOSBox key
                if field not in key_mapping:
                    continue

                # Get the corresponding DOSBox key
                dosbox_key = key_mapping[field]

                # Read the value from the widget and update the config
                if isinstance(widget, Gtk.Switch):  # GtkSwitch
                    value = widget.get_active()
                    self.config[key][dosbox_key] = str(value).lower()  # Convert boolean to 'true'/'false'
                
                elif isinstance(widget, Gtk.ComboBoxText):  # GtkComboBoxText
                    active_text = widget.get_active_text()
                    if active_text:
                        self.config[key][dosbox_key] = active_text
                
                elif isinstance(widget, Gtk.SpinButton):  # GtkSpinButton
                    value = widget.get_value_as_int()
                    self.config[key][dosbox_key] = str(value)
                
                elif isinstance(widget, Gtk.TextView):  # GtkTextView (e.g., autoexec)
                    buffer = widget.get_buffer()
                    start_iter = buffer.get_start_iter()
                    end_iter = buffer.get_end_iter()
                    text = buffer.get_text(start_iter, end_iter, True)

                    # Handle the autoexec section differently to prevent duplicate sections
                    if dosbox_key == "autoexec":
                        if text.strip():  # Only update if there's content
                            if self.config.has_section(dosbox_key):
                                self.config.set_raw_section(dosbox_key, text)
                            else:
                                self.config.add_section(dosbox_key)
                                self.config.set_raw_section(dosbox_key, text)

                elif type(widget) is Gtk.Entry:  # GtkEntry
                    value = widget.get_text()
                    self.config[key][dosbox_key] = value

        # Now, we handle removing sections that have no key-value pairs
        sections_to_remove = []
        for section in self.config.sections():
            # If a section has no key-value pairs, we mark it for removal
            if not self.config[section]:  # Check if section is empty
                sections_to_remove.append(section)

        # Remove the empty sections
        for section in sections_to_remove:
            self.config.remove_section(section)

        # Write the updated configuration to the file
        config_file_path = self.get_file_path()

        # Open the config file and write the updated configuration
        with open(config_file_path, "w") as config_file:
            self.config.write(config_file)

        print(f"Configuration saved to {config_file_path}")


    def do_reload_config(self, button=None):
        self.create_config(self.get_file_path())
        self.load_game_config()
        self.cfg_values = load_config(self.config)
        self.update_ui()

    def load_game_config(self):
        if self.game_opts:
            cf = self.get_file_path()
            print(f"Loading game config: \n\t{cf}")
            self.config.read(cf)
        else:
            print("No game found")

    def do_remove_config(self, button, parent):
        """ Remove config and game listing

            Parameters: button, parent
                - button: The button element that called this method
                - parent: The parent of this window.
        """
        cf = self.get_file_path()
        directory_path, _ = os.path.split(cf)
        try:
            os.remove(cf)
            print(f"Removed game config @ {cf}")
        except FileNotFoundError:
            print(f"File at {cf} not found?")
        except PermissionError:
            print(f"Yeah, so uhh, you can't do that. Failed to remove {cf}")
        except Exception as e:
            print(f"Negatory Batman, {e}")

        if not os.path.exists(cf):
            try:
                with open("games.json", "r") as file:
                    data = json.load(file)

                updated_data = [block for block in data if block["config_file"] != directory_path]

                with open("games.json", "w") as file:
                    json.dump(updated_data, file, indent=4)

                print(f"Block for {cf} removed")
            except FileNotFoundError:
                print(f"JSON file not found: {cf}")
            except KeyError as e:
                print(f"Key error: {e}")
            except json.JSONDecodeError:
                print("Error decoding JSON file.")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        parent.refresh_game_list()
        
    def get_file_path(self):
        """ Get file path of config """


        config_file_path = self.game_opts.config["config_file"]

        label = self.game_opts.get_child().get_text().replace(" ","").lower()
        config_file_name = f"{label}.conf"

        cf = os.path.join(config_file_path, config_file_name)

        # check to see if the file path exists
        if os.path.exists(cf):
            return cf
        else:
            self.create_config(cf)
            return cf

    def create_config(self, cf):
        """ Create a config file """
        with open("./base-config.conf", "r") as reader:
            with open(cf, "w") as writer:
                writer.write(reader.read())

    def update_ui(self):
        """ Update the UI """
        cbox_mappings = ComboBoxMappings()

        for key, val in self.widgets.items():
            for field, widget in val.items():
                section = getattr(self.cfg_values, key)  # Get the section object (e.g., SDLConfig, RenderConfig)
                
                
                # Use getattr to fetch the value for the specific field in that section
                
                value = getattr(section, field, None)  # Default to None if the field doesn't exist

                ## GtkSwitch
                if isinstance(widget, Gtk.Switch):
                    if value is not None:
                        widget.set_active(value)

                ## GtkComboBoxText
                if isinstance(widget, Gtk.ComboBoxText):
                    value_list = getattr(cbox_mappings, field, [])
                    if value is not None and value in value_list:
                        widget.set_active(value_list.index(value))
                    else:
                        widget.set_active(-1)

                ## GtkSpinButton
                if isinstance(widget, Gtk.SpinButton):
                    if value is not None:
                        widget.set_value(value)

                ## GtkTextView
                if isinstance(widget, Gtk.TextView):
                    if value is not None:
                        self.autoexec_buffer.set_text(value)

                ## GtkEntry
                if type(widget) is Gtk.Entry:
                    if value is not None:
                        widget.set_text(value)

                    
                    


        



