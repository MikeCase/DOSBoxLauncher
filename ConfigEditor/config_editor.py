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
    def __init__(self, parent, game = None) -> None:
        """ Main entry point for the ConfigEditor """
        super().__init__(title="DOSBox Config Editor", transient_for=parent)
        self.config = DOSBoxConfigParser()
        self.parent = parent
        self.game_opts = game

        self.setup_ui()
        self.load_game_config()
        self.cfg_values = load_config(self.config)
        self.update_ui()

    def setup_ui(self):
        # Load the editor UI
        builder = Gtk.Builder()
        builder.add_from_file("UI/config_options.ui")

        # Get the window object from the builder
        self.opts_window = builder.get_object("OptsWindow")


        # Not yet sure if I want to map all the buffers.
        self.autoexec_buffer = builder.get_object("autoexec_tbuffer")
        self.serial_buffers = {
            'serial1': builder.get_object("serial1_entry_buffer"),
            'serial2': builder.get_object("serial2_entry_buffer"),
            'serial3': builder.get_object("serial3_entry_buffer"),
            'serial4': builder.get_object("serial4_entry_buffer"),
        }

        self.widgets = {
            "sdl": self._get_widgets(builder, [
                'fullscreen_sw', 'fulldouble_sw', 'full_resolution_cbox', 'wind_res_cbox', 'output_cbox', 'autolock_sw',
                'sensitivity_spin', 'wait_on_error_sw', 'priority_cbox', 'mapper_file_entry', 'use_scan_codes_sw']),
            "dosbox": self._get_widgets(builder, ['language_entry', 'memsize_spin', 'machine_cbox', 'captures_entry']),
            "render": self._get_widgets(builder, ['frameskip_spin', 'aspect_sw', 'scaler_cbox']),
            "cpu": self._get_widgets(builder, ['core_cbox', 'cpu_type_cbox', 'cycles_cbox', 'cycle_up_spin', 'cycle_down_spin']),
            "serial": self._get_widgets(builder, ['serial1_cbox', 'serial2_cbox', 'serial3_cbox', 'serial4_cbox']),
            "dos": self._get_widgets(builder, ['xms_sw', 'ems_sw', 'umb_sw', 'keyboard_layout_cbox']),
            "ipx": self._get_widgets(builder, ['ipx_sw']),
            "autoexec": self._get_widgets(builder, ['autoexec_tbox']),
        }

        
        self._connect_buttons(builder)
        self.opts_window.show()

    def _get_widgets(self, builder, widget_names):
        """ Helper function to get the widgets in each section of the UI.
            
            Args:
                builder: Builder object for the Gtk.Window
                widget_names: List of the names of all the widgets in the window. 
        """
        return {name: builder.get_object(name) for name in widget_names}

    def _connect_buttons(self, builder):
        """ Helper function to connect all the buttons of the window to their signals
            
            Args:
                builder: Builder object for window.
        """
        buttons = {
            "save_config_btn": self.save_config,
            "reload_config_btn": self.do_reload_config,
            "cancel_btn": self.close_window,
            "remove_config_btn": lambda btn: self.do_remove_config(btn, self.parent),
        }
        for btn_name, handler in buttons.items():
            btn = builder.get_object(btn_name)
            btn.connect('clicked', handler)

    def close_window(self, hWnd) -> None:
        """Closes the window

        Args:
            hWnd (_type_): The window that shall be closed.
        """
        self.opts_window.destroy()

    def save_config(self, button=None):
        key_mapping = KEY_MAPPINGS
        widget_handlers = {
            Gtk.Switch: lambda w: str(w.get_active()).lower(),
            Gtk.ComboBoxText: lambda w: w.get_active_text(),
            Gtk.SpinButton: lambda w: str(w.get_value_as_int()),
            Gtk.TextView: lambda w: w.get_buffer().get_text(w.get_buffer().get_start_iter(), w.get_buffer().get_end_iter(), True),
            Gtk.Entry: lambda w: w.get_text(),
        }

        for key, widgets in self.widgets.items():
            for field, widget in widgets.items():
                if field in key_mapping:
                    dosbox_key = key_mapping[field]
                    handler = widget_handlers.get(type(widget))
                    if handler:
                        value = handler(widget)
                        if value:
                            self.config[key][dosbox_key] = value

        self._remove_empty_sections()
        self._write_config()

    def _remove_empty_sections(self):
        for section in list(self.config.sections()):
            if not self.config[section]:
                self.config.remove_section(section)

    def _write_config(self):
        config_file_path = self.get_file_path()
        with open(config_file_path, "w") as config_file:
            self.config.write(config_file)
        print(f"Configuration saved to {config_file_path}")

    def do_reload_config(self, button=None):
        """Helper function to reload the default config when the button is pressed.

        Args:
            button (Gtk.Widget, optional): The button pressed to call this method. Defaults to None.
        """

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

    def do_remove_config(self, button, parent) -> None:
        """Remove the config file.

        Args:
            button (_type_): _description_
            parent (_type_): _description_
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
        widget_handlers = {
            Gtk.Switch: lambda w, v: w.set_active(v),
            Gtk.ComboBoxText: lambda w, v, m: w.set_active(m.index(v) if v in m else -1),
            Gtk.SpinButton: lambda w, v: w.set_value(v),
            Gtk.TextView: lambda w, v: self.autoexec_buffer.set_text(v),
            Gtk.Entry: lambda w, v: w.set_text(v),
        }

        for key, widgets in self.widgets.items():
            section = getattr(self.cfg_values, key)
            for field, widget in widgets.items():
                value = getattr(section, field, None)
                handler = widget_handlers.get(type(widget))
                if handler:
                    if isinstance(widget, Gtk.ComboBoxText):
                        handler(widget, value, getattr(cbox_mappings, field, []))
                    else:
                        handler(widget, value)

                    
                    


        



