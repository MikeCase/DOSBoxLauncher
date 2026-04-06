"""Advanced configuration dialogs for sound and joystick options."""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .dataclasses import (
    COMBO_BOX_MAPPINGS,
    KEY_MAPPINGS,
    SECTION_MAPPINGS,
)
from .tooltips import TOOLTIPS


class SoundAdvancedDialog(Gtk.Dialog):
    """Advanced sound settings dialog."""

    def __init__(self, parent: Gtk.Window, config) -> None:
        super().__init__(
            title="Advanced Sound Settings",
            transient_for=parent,
            flags=0,
        )
        self.parent = parent
        self.main_config = config

        builder = Gtk.Builder()
        builder.add_from_file("UI/sound_advanced.ui")

        self.dialog = builder.get_object("sound_adv_dialog")

        self.widgets = {
            "sound_adv": self._get_widgets(
                builder,
                [
                    "sbbase_cbox",
                    "sb_hdma_spin",
                    "sbmixer_sw",
                    "mpu401_cbox",
                    "oplmode_cbox",
                    "oplemu_cbox",
                    "opl_rate_spin",
                ],
            )
        }

        save_btn = builder.get_object("sound_adv_save_btn")
        cancel_btn = builder.get_object("sound_adv_cancel_btn")

        save_btn.connect("clicked", self._on_save)
        cancel_btn.connect("clicked", self._on_cancel)

        self._update_ui()
        self._set_tooltips()
        self.dialog.show()

    def _get_widgets(self, builder: Gtk.Builder, names: list[str]) -> dict[str, Gtk.Widget]:
        return {name: builder.get_object(name) for name in names if builder.get_object(name)}

    def _set_tooltips(self) -> None:
        """Set tooltips on all widgets that have tooltip text defined."""
        for widgets in self.widgets.values():
            for widget_name, widget in widgets.items():
                if widget_name in TOOLTIPS:
                    widget.set_tooltip_text(TOOLTIPS[widget_name])

    def _update_ui(self) -> None:
        if not self.main_config or not hasattr(self.main_config, "sound_adv"):
            return

        section_data = self.main_config.sound_adv
        widget_handlers = {
            Gtk.Switch: lambda w, v: w.set_active(bool(v)),
            Gtk.ComboBoxText: lambda w, v, m: w.set_active(m.index(v) if v in m else -1),
            Gtk.SpinButton: lambda w, v: w.set_value(int(v) if v else 0),
        }

        for field, widget in self.widgets.get("sound_adv", {}).items():
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

    def run(self) -> None:
        self.dialog.run()

    def _on_save(self, btn: Gtk.Button) -> None:
        widget_handlers = {
            Gtk.Switch: lambda w: str(w.get_active()).lower(),
            Gtk.ComboBoxText: lambda w: w.get_active_text() or "",
            Gtk.SpinButton: lambda w: str(w.get_value_as_int()),
        }

        for section, widgets in self.widgets.items():
            for field, widget in widgets.items():
                if field in KEY_MAPPINGS:
                    dosbox_key = KEY_MAPPINGS[field]
                    handler = widget_handlers.get(type(widget))
                    if handler:
                        value = handler(widget)
                        if value:
                            config_section = SECTION_MAPPINGS.get(section, section)
                            if field == "mpu401_cbox":
                                config_section = "midi"

                            if config_section not in self.parent.config.sections():
                                self.parent.config.add_section(config_section)
                            self.parent.config[config_section][dosbox_key] = value

        if self.parent.config.has_section("sound"):
            self.parent.config.remove_section("sound")

        self._write_config()
        self.dialog.destroy()

    def _on_cancel(self, btn: Gtk.Button) -> None:
        self.dialog.destroy()

    def _write_config(self) -> None:
        config_file_path = self.parent._get_config_file_path()
        with open(config_file_path, "w") as f:
            self.parent.config.write(f)


class JoystickAdvancedDialog(Gtk.Dialog):
    """Advanced joystick settings dialog."""

    def __init__(self, parent: Gtk.Window, config) -> None:
        super().__init__(
            title="Advanced Joystick Settings",
            transient_for=parent,
            flags=0,
        )
        self.parent = parent
        self.main_config = config

        builder = Gtk.Builder()
        builder.add_from_file("UI/joystick_advanced.ui")

        self.dialog = builder.get_object("joystick_adv_dialog")

        self.widgets = {
            "joystick_adv": self._get_widgets(
                builder,
                [
                    "timed_sw",
                    "swap34_sw",
                    "buttonwrap_sw",
                    "joy_x_axis_spin",
                    "joy_y_axis_spin",
                ],
            )
        }

        save_btn = builder.get_object("joystick_adv_save_btn")
        cancel_btn = builder.get_object("joystick_adv_cancel_btn")

        save_btn.connect("clicked", self._on_save)
        cancel_btn.connect("clicked", self._on_cancel)

        self._update_ui()
        self._set_tooltips()
        self.dialog.show()

    def _get_widgets(self, builder: Gtk.Builder, names: list[str]) -> dict[str, Gtk.Widget]:
        return {name: builder.get_object(name) for name in names if builder.get_object(name)}

    def _set_tooltips(self) -> None:
        """Set tooltips on all widgets that have tooltip text defined."""
        for widgets in self.widgets.values():
            for widget_name, widget in widgets.items():
                if widget_name in TOOLTIPS:
                    widget.set_tooltip_text(TOOLTIPS[widget_name])

    def _update_ui(self) -> None:
        if not self.main_config or not hasattr(self.main_config, "joystick_adv"):
            return

        section_data = self.main_config.joystick_adv
        widget_handlers = {
            Gtk.Switch: lambda w, v: w.set_active(bool(v)),
            Gtk.SpinButton: lambda w, v: w.set_value(int(v) if v else 0),
        }

        for field, widget in self.widgets.get("joystick_adv", {}).items():
            value = getattr(section_data, field, None)
            if value is None:
                continue

            handler = widget_handlers.get(type(widget))
            if handler:
                handler(widget, value)

    def run(self) -> None:
        self.dialog.run()

    def _on_save(self, btn: Gtk.Button) -> None:
        widget_handlers = {
            Gtk.Switch: lambda w: str(w.get_active()).lower(),
            Gtk.SpinButton: lambda w: str(w.get_value_as_int()),
        }

        for section, widgets in self.widgets.items():
            for field, widget in widgets.items():
                if field in KEY_MAPPINGS:
                    dosbox_key = KEY_MAPPINGS[field]
                    handler = widget_handlers.get(type(widget))
                    if handler:
                        value = handler(widget)
                        if value:
                            if section not in ("joystick",):
                                section = "joystick"
                            if section not in self.parent.config.sections():
                                self.parent.config.add_section(section)
                            self.parent.config[section][dosbox_key] = value

        self._write_config()
        self.dialog.destroy()

    def _on_cancel(self, btn: Gtk.Button) -> None:
        self.dialog.destroy()

    def _write_config(self) -> None:
        config_file_path = self.parent._get_config_file_path()
        with open(config_file_path, "w") as f:
            self.parent.config.write(f)
