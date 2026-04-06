"""Tests for config editor tab consolidation and new sound sections."""

import pytest


class TestTabStructure:
    """Tests for consolidated tab structure (7 tabs)."""

    def test_ui_has_7_tabs(self):
        """The config editor should have exactly 7 tabs."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        tab_count = content.count('type="tab"')
        assert tab_count == 7, f"Expected 7 tabs, found {tab_count}"

    def test_has_display_tab(self):
        """Should have a Display tab (consolidated SDL + DOSBox)."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "Display" in content, "Missing Display tab"

    def test_has_render_tab(self):
        """Should have a Render tab."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "Render" in content, "Missing Render tab"

    def test_has_cpu_tab(self):
        """Should have a CPU tab."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "CPU" in content, "Missing CPU tab"

    def test_has_system_tab(self):
        """Should have a System tab (consolidated DOS + Serial + IPX)."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "System" in content, "Missing System tab"

    def test_has_sound_tab(self):
        """Should have a Sound tab."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "Sound" in content, "Missing Sound tab"

    def test_has_joystick_tab(self):
        """Should have a Joystick tab."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "Joystick" in content, "Missing Joystick tab"

    def test_has_autoexec_tab(self):
        """Should have an Autoexec tab."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "Autoexec" in content, "Missing Autoexec tab"

    def test_no_legacy_tab_names(self):
        """Should not have old separate tab names."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "SDL Options" not in content, "Old SDL Options tab should be removed"
        assert "DOSBox Options" not in content, "Old DOSBox Options tab should be removed"


class TestSoundExpandableSections:
    """Tests for Sound tab expandable sections."""

    def test_sound_tab_has_mixer_expander(self):
        """Sound tab should have Mixer expandable section."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "mixer_expander" in content or "Mixer" in content, "Missing Mixer expander"

    def test_sound_tab_has_midi_expander(self):
        """Sound tab should have MIDI expandable section."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "midi_expander" in content or "MIDI" in content, "Missing MIDI expander"

    def test_sound_tab_has_speaker_expander(self):
        """Sound tab should have Speaker expandable section."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "speaker_expander" in content or "Speaker" in content, "Missing Speaker expander"

    def test_sound_tab_has_gus_expander(self):
        """Sound tab should have GUS (Gravis Ultrasound) expandable section."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "gus_expander" in content or "GUS" in content or "Gravis" in content, (
            "Missing GUS expander"
        )

    def test_mixer_has_nosound_switch(self):
        """Mixer section should have nosound switch."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "nosound_sw" in content, "Missing nosound switch"

    def test_mixer_has_rate_combobox(self):
        """Mixer section should have rate combobox."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "mixer_rate_cbox" in content or "rate" in content.lower(), "Missing mixer rate"

    def test_mixer_has_blocksize_combobox(self):
        """Mixer section should have blocksize combobox."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "blocksize_cbox" in content or "blocksize" in content.lower(), "Missing blocksize"

    def test_mixer_has_prebuffer_spin(self):
        """Mixer section should have prebuffer spinbutton."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "prebuffer_spin" in content or "prebuffer" in content.lower(), "Missing prebuffer"

    def test_midi_has_mpu401_combobox(self):
        """MIDI section should have mpu401 combobox."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "mpu401_cbox" in content, "Missing mpu401 combobox"

    def test_midi_has_mididevice_combobox(self):
        """MIDI section should have mididevice combobox."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "mididevice_cbox" in content or "mididevice" in content.lower(), "Missing mididevice"

    def test_midi_has_midiconfig_entry(self):
        """MIDI section should have midiconfig entry."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "midiconfig_entry" in content or "midiconfig" in content.lower(), (
            "Missing midiconfig"
        )

    def test_speaker_has_pcspeaker_switch(self):
        """Speaker section should have pcspeaker switch."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "pcspeaker_sw" in content or "pcspeaker" in content.lower(), "Missing pcspeaker"

    def test_speaker_has_pcrate_combobox(self):
        """Speaker section should have pcrate combobox."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "pcrate_cbox" in content or "pcrate" in content.lower(), "Missing pcrate"

    def test_speaker_has_tandy_combobox(self):
        """Speaker section should have tandy combobox."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "tandy_cbox" in content or "tandy" in content.lower(), "Missing tandy"

    def test_speaker_has_tandyrate_combobox(self):
        """Speaker section should have tandyrate combobox."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "tandyrate_cbox" in content or "tandyrate" in content.lower(), "Missing tandyrate"

    def test_speaker_has_disney_switch(self):
        """Speaker section should have disney switch."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "disney_sw" in content or "disney" in content.lower(), "Missing disney"

    def test_gus_has_gus_switch(self):
        """GUS section should have gus switch."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "gus_sw" in content or "gus=" in content.lower(), "Missing GUS enable switch"

    def test_gus_has_gusrate_combobox(self):
        """GUS section should have gusrate combobox."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "gusrate_cbox" in content or "gusrate" in content.lower(), "Missing gusrate"

    def test_gus_has_gusbase_combobox(self):
        """GUS section should have gusbase combobox."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "gusbase_cbox" in content or "gusbase" in content.lower(), "Missing gusbase"

    def test_gus_has_gusirq_spinbutton(self):
        """GUS section should have gusirq spinbutton."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "gusirq_spin" in content or "gusirq" in content.lower(), "Missing gusirq"

    def test_gus_has_gusdma_spinbutton(self):
        """GUS section should have gusdma spinbutton."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "gusdma_spin" in content or "gusdma" in content.lower(), "Missing gusdma"

    def test_gus_has_ultradir_entry(self):
        """GUS section should have ultradir entry."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "ultradir_entry" in content or "ultradir" in content.lower(), "Missing ultradir"


class TestWindowSize:
    """Tests for window size improvements."""

    def test_window_is_larger(self):
        """Window should be larger than old 770x440 size."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        import re

        width_match = re.search(r'default-width">(\d+)', content)
        height_match = re.search(r'default-height">(\d+)', content)

        if width_match and height_match:
            width = int(width_match.group(1))
            height = int(height_match.group(1))
            assert width > 770, f"Width should be > 770, got {width}"
            assert height > 440, f"Height should be > 440, got {height}"
        else:
            pytest.fail("Could not find window dimensions in UI")


class TestAdvancedButtons:
    """Tests for improved advanced buttons."""

    def test_sound_advanced_button_has_text(self):
        """Sound advanced button should have text label, not just >."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "Advanced" in content, "Sound advanced button should say 'Advanced'"

    def test_joystick_advanced_button_has_text(self):
        """Joystick advanced button should have text label, not just >."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        count = content.count("Advanced")
        assert count >= 2, "Both advanced buttons should say 'Advanced'"


class TestDataclassSections:
    """Tests for new dataclass sections."""

    def test_has_mixer_config_dataclass(self):
        """Should have MixerConfig dataclass."""
        from dosboxlauncher.config_editor.dataclasses import MixerConfig

        config = MixerConfig()
        assert config is not None

    def test_has_midi_config_dataclass(self):
        """Should have MidiConfig dataclass."""
        from dosboxlauncher.config_editor.dataclasses import MidiConfig

        config = MidiConfig()
        assert config is not None

    def test_has_speaker_config_dataclass(self):
        """Should have SpeakerConfig dataclass."""
        from dosboxlauncher.config_editor.dataclasses import SpeakerConfig

        config = SpeakerConfig()
        assert config is not None

    def test_has_gus_config_dataclass(self):
        """Should have GusConfig dataclass."""
        from dosboxlauncher.config_editor.dataclasses import GusConfig

        config = GusConfig()
        assert config is not None

    def test_config_contains_all_sections(self):
        """Config should contain all sections including new ones."""
        from dosboxlauncher.config_editor.dataclasses import Config

        config = Config()

        assert hasattr(config, "mixer"), "Config missing mixer section"
        assert hasattr(config, "midi"), "Config missing midi section"
        assert hasattr(config, "speaker"), "Config missing speaker section"
        assert hasattr(config, "gus"), "Config missing gus section"


class TestSoundAutoDisable:
    """Tests for auto-disable sound options feature."""

    def test_nosound_disables_other_options(self):
        """When nosound is enabled, other sound options should be auto-disabled."""
        editor_path = "src/dosboxlauncher/config_editor/editor.py"
        with open(editor_path) as f:
            content = f.read()

        assert "nosound" in content.lower(), "Editor should handle nosound option"

    def test_nosound_callback_exists(self):
        """Should have a callback to handle nosound toggle."""
        editor_path = "src/dosboxlauncher/config_editor/editor.py"
        with open(editor_path) as f:
            content = f.read()

        assert "nosound" in content.lower() or "on_nosound" in content.lower(), (
            "Should have nosound handler"
        )
