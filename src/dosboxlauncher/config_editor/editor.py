"""DOSBox configuration editor window."""

import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ..config import get_games_dir
from ..models import Game
from .dataclasses import COMBO_BOX_MAPPINGS, KEY_MAPPINGS, SECTION_MAPPINGS, Config, load_config
from .parser import DOSBoxConfigParser
from .tooltips import TOOLTIPS

DEFAULT_CONFIG = "base-config.conf"


class ConfigEditor(Gtk.Window):
    """Window for editing DOSBox configuration files."""

    def __init__(self, parent: Gtk.Window, game: Game) -> None:
        super().__init__(title="DOSBox Config Editor", transient_for=parent)
        self.parent = parent
        self.game = game
        self.config = DOSBoxConfigParser()
        self.cfg_values: Config | None = None

        self._setup_ui()
        self._load_game_config()
        self._update_ui()

    def _setup_ui(self) -> None:
        """Load and setup the UI from builder."""
        builder = Gtk.Builder()
        builder.add_from_file("UI/config_options.ui")

        self.opts_window = builder.get_object("OptsWindow")

        self.autoexec_buffer = builder.get_object("autoexec_tbuffer")
        self.serial_buffers = {
            name: builder.get_object(f"{name}_entry_buffer")
            for name in ["serial1", "serial2", "serial3", "serial4"]
        }

        self.widgets: dict[str, dict[str, Gtk.Widget]] = {
            "sdl": self._get_widgets(
                builder,
                [
                    "fullscreen_sw",
                    "fulldouble_sw",
                    "full_resolution_cbox",
                    "wind_res_cbox",
                    "output_cbox",
                    "autolock_sw",
                    "sensitivity_spin",
                    "wait_on_error_sw",
                    "priority_cbox",
                    "mapper_file_entry",
                    "use_scan_codes_sw",
                ],
            ),
            "dosbox": self._get_widgets(
                builder, ["language_entry", "memsize_spin", "machine_cbox", "captures_entry"]
            ),
            "render": self._get_widgets(builder, ["frameskip_spin", "aspect_sw", "scaler_cbox"]),
            "cpu": self._get_widgets(
                builder,
                ["core_cbox", "cpu_type_cbox", "cycles_cbox", "cycle_up_spin", "cycle_down_spin"],
            ),
            "serial": self._get_widgets(
                builder, ["serial1_cbox", "serial2_cbox", "serial3_cbox", "serial4_cbox"]
            ),
            "dos": self._get_widgets(
                builder, ["xms_sw", "ems_sw", "umb_sw", "keyboard_layout_cbox"]
            ),
            "ipx": self._get_widgets(builder, ["ipx_sw"]),
            "autoexec": self._get_widgets(builder, ["autoexec_tbox"]),
            "sound": self._get_widgets(builder, ["sbtype_cbox", "sb_irq_spin", "sb_dma_spin"]),
            "mixer": self._get_widgets(
                builder,
                ["nosound_sw", "mixer_rate_cbox", "blocksize_cbox", "prebuffer_spin"],
            ),
            "midi": self._get_widgets(
                builder,
                ["mpu401_cbox", "mididevice_cbox", "midiconfig_entry"],
            ),
            "speaker": self._get_widgets(
                builder,
                ["pcspeaker_sw", "pcrate_cbox", "tandy_cbox", "tandyrate_cbox", "disney_sw"],
            ),
            "gus": self._get_widgets(
                builder,
                [
                    "gus_sw",
                    "gusrate_cbox",
                    "gusbase_cbox",
                    "gusirq_spin",
                    "gusdma_spin",
                    "ultradir_entry",
                ],
            ),
            "joystick": self._get_widgets(builder, ["joysticktype_cbox", "autofire_sw"]),
        }
        self.sound_containers = self._get_widgets(builder, ["sound_adv_btn"])

        self._connect_buttons(builder)
        self._connect_advanced_buttons(builder)
        self._connect_sound_controls(builder)
        self._set_tooltips()
        self.opts_window.show()

    def _get_widgets(self, builder: Gtk.Builder, names: list[str]) -> dict[str, Gtk.Widget]:
        """Get widgets by name from builder."""
        return {name: builder.get_object(name) for name in names if builder.get_object(name)}

    def _set_tooltips(self) -> None:
        """Set tooltips on all widgets that have tooltip text defined."""
        for widgets in self.widgets.values():
            for widget_name, widget in widgets.items():
                if widget_name in TOOLTIPS:
                    widget.set_tooltip_text(TOOLTIPS[widget_name])

    def _connect_buttons(self, builder: Gtk.Builder) -> None:
        """Connect button signals."""
        buttons = {
            "save_config_btn": self._save_config,
            "reset_config_btn": self._reset_config,
            "cancel_btn": self._close_window,
            "remove_config_btn": lambda btn: self._remove_config(btn, self.parent),
        }
        for name, handler in buttons.items():
            btn = builder.get_object(name)
            if btn:
                btn.connect("clicked", handler)

    def _connect_advanced_buttons(self, builder: Gtk.Builder) -> None:
        """Connect advanced settings buttons."""
        sound_adv_btn = builder.get_object("sound_adv_btn")
        joystick_adv_btn = builder.get_object("joystick_adv_btn")

        if sound_adv_btn:
            sound_adv_btn.connect("clicked", self._open_sound_advanced)
        if joystick_adv_btn:
            joystick_adv_btn.connect("clicked", self._open_joystick_advanced)

    def _connect_sound_controls(self, builder: Gtk.Builder) -> None:
        """Connect sound-specific UI behaviors."""
        nosound_sw = builder.get_object("nosound_sw")
        if nosound_sw:
            nosound_sw.connect("notify::active", self._on_nosound_toggled)

    def _open_sound_advanced(self, btn: Gtk.Widget) -> None:
        """Open advanced sound settings dialog."""
        from .advanced_dialogs import SoundAdvancedDialog

        dialog = SoundAdvancedDialog(self, self.cfg_values)
        dialog.run()

    def _open_joystick_advanced(self, btn: Gtk.Widget) -> None:
        """Open advanced joystick settings dialog."""
        from .advanced_dialogs import JoystickAdvancedDialog

        dialog = JoystickAdvancedDialog(self, self.cfg_values)
        dialog.run()

    def _close_window(self, btn: Gtk.Widget) -> None:
        """Close the window."""
        self.opts_window.destroy()

    def _save_config(self, btn: Gtk.Widget | None = None) -> None:
        """Save configuration to file."""
        widget_handlers = {
            Gtk.Switch: lambda w: str(w.get_active()).lower(),
            Gtk.ComboBoxText: lambda w: w.get_active_text() or "",
            Gtk.SpinButton: lambda w: str(w.get_value_as_int()),
            Gtk.TextView: lambda w: w.get_buffer().get_text(
                w.get_buffer().get_start_iter(), w.get_buffer().get_end_iter(), True
            ),
            Gtk.Entry: lambda w: w.get_text(),
        }

        for section, widgets in self.widgets.items():
            if section == "autoexec":
                continue

            config_section = self._get_config_section_name(section)

            for field, widget in widgets.items():
                if field in KEY_MAPPINGS:
                    dosbox_key = KEY_MAPPINGS[field]
                    handler = widget_handlers.get(type(widget))
                    if handler:
                        value = handler(widget)
                        if value:
                            if config_section not in self.config.sections():
                                self.config.add_section(config_section)
                            self.config[config_section][dosbox_key] = value

        autoexec_widgets = self.widgets.get("autoexec", {})
        if "autoexec_tbox" in autoexec_widgets:
            widget = autoexec_widgets["autoexec_tbox"]
            handler = widget_handlers.get(type(widget))
            if handler:
                value = handler(widget)
                self.config.set_raw_section("autoexec", value or "")

        self._remove_empty_sections()
        self._write_config()

    def _remove_empty_sections(self) -> None:
        """Remove empty sections from config."""
        if self.config.has_section("sound"):
            self.config.remove_section("sound")

        for section in list(self.config.sections()):
            if not self.config[section]:
                self.config.remove_section(section)

    def _write_config(self) -> None:
        """Write config to file."""
        config_file_path = self._get_config_file_path()
        with open(config_file_path, "w") as f:
            self.config.write(f)

    def _reset_config(self, btn: Gtk.Widget | None = None) -> None:
        """Reset configuration to defaults with confirmation dialog."""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Reset Configuration to Defaults?",
        )
        dialog.format_secondary_text(
            "This will replace all settings with default values. This action cannot be undone."
        )

        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            self._create_config(self._get_config_file_path())
            self._load_game_config()
            self.cfg_values = load_config(self.config)
            self._update_ui()

    def _load_game_config(self) -> None:
        """Load the game's config file."""
        config_path = self._get_config_file_path()
        self.config = DOSBoxConfigParser()

        if os.path.exists(config_path):
            self.config.read(config_path)
        else:
            self._create_config(config_path)
            self.config.read(config_path)

    def _remove_config(self, btn: Gtk.Widget, parent: Gtk.Window) -> None:
        """Remove the config file and game from library."""
        config_path = self._get_config_file_path()
        try:
            if os.path.exists(config_path):
                os.remove(config_path)
        except OSError:
            pass  # Silent failure - file may already be removed

    def _get_config_file_path(self) -> str:
        """Get the config file path for this game."""
        return self.game.get_config_file_path()

    def _create_config(self, config_path: str) -> None:
        """Create a new config file from default."""
        games_dir = get_games_dir()
        default_config = games_dir / DEFAULT_CONFIG
        if not default_config.exists():
            default_config = DEFAULT_CONFIG

        with open(default_config) as reader:
            with open(config_path, "w") as writer:
                writer.write(reader.read())

    def _get_config_section_name(self, section: str) -> str:
        """Map UI section names to DOSBox config section names."""
        return SECTION_MAPPINGS.get(section, section)

    def _on_nosound_toggled(self, widget: Gtk.Switch, _param) -> None:
        """Disable sound-related controls when silent mode is enabled."""
        self._update_sound_controls(widget.get_active())

    def _update_sound_controls(self, nosound_enabled: bool) -> None:
        """Enable or disable sound widgets based on silent mode."""
        disabled_sections = ["sound", "midi", "speaker", "gus"]

        for section in disabled_sections:
            for widget in self.widgets.get(section, {}).values():
                widget.set_sensitive(not nosound_enabled)

        for container in self.sound_containers.values():
            container.set_sensitive(not nosound_enabled)

        for widget_name in ("mixer_rate_cbox", "blocksize_cbox", "prebuffer_spin"):
            widget = self.widgets.get("mixer", {}).get(widget_name)
            if widget:
                widget.set_sensitive(not nosound_enabled)

    def _update_ui(self) -> None:
        """Update UI with config values."""
        self.cfg_values = load_config(self.config)

        widget_handlers = {
            Gtk.Switch: lambda w, v: w.set_active(bool(v)),
            Gtk.ComboBoxText: lambda w, v, m: w.set_active(m.index(v) if v in m else -1),
            Gtk.SpinButton: lambda w, v: w.set_value(int(v) if v else 0),
            Gtk.TextView: lambda w, v: self.autoexec_buffer.set_text(v or ""),
            Gtk.Entry: lambda w, v: w.set_text(v or ""),
        }

        for section, widgets in self.widgets.items():
            section_data = getattr(self.cfg_values, section, None)
            if section_data is None:
                continue

            for field, widget in widgets.items():
                value = getattr(section_data, field, None)
                if value is None:
                    continue

                handler = widget_handlers.get(type(widget))
                if handler:
                    if isinstance(widget, Gtk.ComboBoxText):
                        mappings = COMBO_BOX_MAPPINGS.get(field, [])
                        handler(widget, value, mappings)
                    else:
                        handler(widget, value)

        nosound_widget = self.widgets.get("mixer", {}).get("nosound_sw")
        if nosound_widget:
            self._update_sound_controls(nosound_widget.get_active())
