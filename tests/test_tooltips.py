"""Tests for DOSBox configuration editor tooltips."""

from dosboxlauncher.config_editor.tooltips import TOOLTIPS

SDL_TAB_WIDGETS = [
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
]

DOSBOX_TAB_WIDGETS = [
    "language_entry",
    "memsize_spin",
    "machine_cbox",
    "captures_entry",
]

RENDER_TAB_WIDGETS = [
    "frameskip_spin",
    "aspect_sw",
    "scaler_cbox",
]

CPU_TAB_WIDGETS = [
    "core_cbox",
    "cpu_type_cbox",
    "cycles_cbox",
    "cycle_up_spin",
    "cycle_down_spin",
]

SERIAL_TAB_WIDGETS = [
    "serial1_cbox",
    "serial2_cbox",
    "serial3_cbox",
    "serial4_cbox",
]

DOS_TAB_WIDGETS = [
    "xms_sw",
    "ems_sw",
    "umb_sw",
    "keyboard_layout_cbox",
]

IPX_TAB_WIDGETS = [
    "ipx_sw",
]

AUTOEXEC_TAB_WIDGETS = [
    "autoexec_tbox",
]

SOUND_BASIC_WIDGETS = [
    "sbtype_cbox",
    "sb_irq_spin",
    "sb_dma_spin",
]

JOYSTICK_BASIC_WIDGETS = [
    "joysticktype_cbox",
    "autofire_sw",
]

SOUND_ADVANCED_WIDGETS = [
    "sbbase_cbox",
    "sb_hdma_spin",
    "sbmixer_sw",
    "mpu401_cbox",
    "oplmode_cbox",
    "oplemu_cbox",
    "opl_rate_spin",
]

JOYSTICK_ADVANCED_WIDGETS = [
    "timed_sw",
    "swap34_sw",
    "buttonwrap_sw",
    "joy_x_axis_spin",
    "joy_y_axis_spin",
]

MIXER_WIDGETS = [
    "nosound_sw",
    "mixer_rate_cbox",
    "blocksize_cbox",
    "prebuffer_spin",
]

MIDI_WIDGETS = [
    "mpu401_cbox",
    "mididevice_cbox",
    "midiconfig_entry",
]

SPEAKER_WIDGETS = [
    "pcspeaker_sw",
    "pcrate_cbox",
    "tandy_cbox",
    "tandyrate_cbox",
    "disney_sw",
]

GUS_WIDGETS = [
    "gus_sw",
    "gusrate_cbox",
    "gusbase_cbox",
    "gusirq_spin",
    "gusdma_spin",
    "ultradir_entry",
]


class TestTooltipsModule:
    def test_tooltips_module_imports(self):
        """TOOLTIPS can be imported from tooltips module."""
        from dosboxlauncher.config_editor.tooltips import TOOLTIPS

        assert TOOLTIPS is not None

    def test_tooltips_is_dict(self):
        """TOOLTIPS is a dictionary."""
        assert isinstance(TOOLTIPS, dict)

    def test_tooltips_count(self):
        """TOOLTIPS has approximately 50 entries."""
        assert len(TOOLTIPS) >= 45


class TestTooltipsContent:
    def test_tooltips_all_non_empty(self):
        """All tooltip entries have non-empty strings."""
        for widget_name, tooltip_text in TOOLTIPS.items():
            assert tooltip_text, f"Empty tooltip for {widget_name}"
            assert len(tooltip_text.strip()) > 0

    def test_tooltips_min_length(self):
        """Tooltips have meaningful length (more than 10 characters)."""
        short_tooltips = [name for name, text in TOOLTIPS.items() if len(text) < 10]
        assert not short_tooltips, f"Too short: {short_tooltips}"


class TestTooltipsCoverage:
    def test_sdl_tab_tooltips(self):
        """All SDL tab widgets have tooltips."""
        for widget in SDL_TAB_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_dosbox_tab_tooltips(self):
        """All DOSBox tab widgets have tooltips."""
        for widget in DOSBOX_TAB_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_render_tab_tooltips(self):
        """All Render tab widgets have tooltips."""
        for widget in RENDER_TAB_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_cpu_tab_tooltips(self):
        """All CPU tab widgets have tooltips."""
        for widget in CPU_TAB_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_serial_tab_tooltips(self):
        """All Serial tab widgets have tooltips."""
        for widget in SERIAL_TAB_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_dos_tab_tooltips(self):
        """All DOS tab widgets have tooltips."""
        for widget in DOS_TAB_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_ipx_tab_tooltips(self):
        """All IPX tab widgets have tooltips."""
        for widget in IPX_TAB_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_autoexec_tab_tooltips(self):
        """All Autoexec tab widgets have tooltips."""
        for widget in AUTOEXEC_TAB_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_sound_basic_tooltips(self):
        """All Sound basic widgets have tooltips."""
        for widget in SOUND_BASIC_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_joystick_basic_tooltips(self):
        """All Joystick basic widgets have tooltips."""
        for widget in JOYSTICK_BASIC_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_sound_advanced_tooltips(self):
        """All Sound advanced widgets have tooltips."""
        for widget in SOUND_ADVANCED_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_mixer_tooltips(self):
        """All Mixer widgets have tooltips."""
        for widget in MIXER_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_midi_tooltips(self):
        """All MIDI widgets have tooltips."""
        for widget in MIDI_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_speaker_tooltips(self):
        """All Speaker widgets have tooltips."""
        for widget in SPEAKER_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_gus_tooltips(self):
        """All GUS widgets have tooltips."""
        for widget in GUS_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"

    def test_joystick_advanced_tooltips(self):
        """All Joystick advanced widgets have tooltips."""
        for widget in JOYSTICK_ADVANCED_WIDGETS:
            assert widget in TOOLTIPS, f"Missing tooltip for {widget}"


class TestTooltipsQuality:
    def test_sdl_tooltips_descriptive(self):
        """SDL tooltips mention relevant options."""
        assert "fullscreen" in TOOLTIPS["fullscreen_sw"].lower()
        assert "ALT" in TOOLTIPS["fullscreen_sw"]

    def test_dosbox_tooltips_descriptive(self):
        """DOSBox tooltips mention machine types."""
        tooltip = TOOLTIPS["machine_cbox"]
        assert "vga" in tooltip.lower() or "svga" in tooltip.lower()

    def test_cpu_tooltips_descriptive(self):
        """CPU tooltips mention cycles and core options."""
        assert "cycles" in TOOLTIPS["cycles_cbox"].lower()
        assert "core" in TOOLTIPS["core_cbox"].lower()

    def test_sound_tooltips_mention_options(self):
        """Sound tooltips list available options."""
        tooltip = TOOLTIPS["sbtype_cbox"]
        assert "sb16" in tooltip or "sb1" in tooltip

    def test_joystick_tooltips_mention_options(self):
        """Joystick tooltips list available options."""
        tooltip = TOOLTIPS["joysticktype_cbox"]
        assert "auto" in tooltip.lower()
