"""Tests for DOSBox configuration dataclasses."""


from dosboxlauncher.config_editor.dataclasses import (
    COMBO_BOX_MAPPINGS,
    KEY_MAPPINGS,
    AutoExecConfig,
    Config,
    CPUConfig,
    DosboxConfig,
    DosConfig,
    GusConfig,
    IpxConfig,
    JoystickAdvConfig,
    JoystickConfig,
    MidiConfig,
    MixerConfig,
    RenderConfig,
    SDLConfig,
    SerialConfig,
    SoundAdvConfig,
    SoundConfig,
    SpeakerConfig,
    load_config,
)
from dosboxlauncher.config_editor.parser import DOSBoxConfigParser


class TestConfigDataclasses:
    def test_sdl_config_defaults(self):
        config = SDLConfig()
        assert config.fullscreen_sw is False
        assert config.fulldouble_sw is False
        assert config.full_resolution_cbox == "original"
        assert config.wind_res_cbox == "original"
        assert config.output_cbox == "surface"
        assert config.autolock_sw is True
        assert config.sensitivity_spin == 1
        assert config.wait_on_error_sw is True
        assert config.priority_cbox == "higher,normal"
        assert config.mapper_file_entry == ""
        assert config.use_scan_codes_sw is False

    def test_dosbox_config_defaults(self):
        config = DosboxConfig()
        assert config.language_entry == ""
        assert config.machine_cbox == "svga_s3"
        assert config.captures_entry == ""
        assert config.memsize_spin == 16

    def test_render_config_defaults(self):
        config = RenderConfig()
        assert config.frameskip_spin == 0
        assert config.aspect_sw is False
        assert config.scaler_cbox == "none"

    def test_cpu_config_defaults(self):
        config = CPUConfig()
        assert config.core_cbox == "auto"
        assert config.cpu_type_cbox == "auto"
        assert config.cycles_cbox == "auto"
        assert config.cycle_up_spin == 10
        assert config.cycle_down_spin == 10

    def test_serial_config_defaults(self):
        config = SerialConfig()
        assert config.serial1_cbox == "disabled"
        assert config.serial2_cbox == "disabled"
        assert config.serial3_cbox == "disabled"
        assert config.serial4_cbox == "disabled"

    def test_dos_config_defaults(self):
        config = DosConfig()
        assert config.xms_sw is True
        assert config.ems_sw is True
        assert config.umb_sw is True
        assert config.keyboard_layout_cbox == "auto"

    def test_ipx_config_defaults(self):
        config = IpxConfig()
        assert config.ipx_sw is False

    def test_autoexec_config_defaults(self):
        config = AutoExecConfig()
        assert config.autoexec_tbox == ""

    def test_config_container(self):
        config = Config()
        assert isinstance(config.sdl, SDLConfig)
        assert isinstance(config.dosbox, DosboxConfig)
        assert isinstance(config.render, RenderConfig)
        assert isinstance(config.cpu, CPUConfig)
        assert isinstance(config.serial, SerialConfig)
        assert isinstance(config.dos, DosConfig)
        assert isinstance(config.ipx, IpxConfig)
        assert isinstance(config.autoexec, AutoExecConfig)


class TestComboBoxMappings:
    def test_full_resolution_cbox(self):
        assert "original" in COMBO_BOX_MAPPINGS["full_resolution_cbox"]
        assert "640x480" in COMBO_BOX_MAPPINGS["full_resolution_cbox"]
        assert "1920x1024" in COMBO_BOX_MAPPINGS["full_resolution_cbox"]

    def test_output_cbox(self):
        assert "surface" in COMBO_BOX_MAPPINGS["output_cbox"]
        assert "opengl" in COMBO_BOX_MAPPINGS["output_cbox"]
        assert "ddraw" in COMBO_BOX_MAPPINGS["output_cbox"]

    def test_machine_cbox(self):
        assert "svga_s3" in COMBO_BOX_MAPPINGS["machine_cbox"]
        assert "vgaonly" in COMBO_BOX_MAPPINGS["machine_cbox"]
        assert "hercules" in COMBO_BOX_MAPPINGS["machine_cbox"]

    def test_scaler_cbox(self):
        assert "none" in COMBO_BOX_MAPPINGS["scaler_cbox"]
        assert "normal2x" in COMBO_BOX_MAPPINGS["scaler_cbox"]
        assert "hq2x" in COMBO_BOX_MAPPINGS["scaler_cbox"]

    def test_core_cbox(self):
        assert "auto" in COMBO_BOX_MAPPINGS["core_cbox"]
        assert "dynamic" in COMBO_BOX_MAPPINGS["core_cbox"]

    def test_cycles_cbox(self):
        assert "auto" in COMBO_BOX_MAPPINGS["cycles_cbox"]
        assert "max" in COMBO_BOX_MAPPINGS["cycles_cbox"]

    def test_serial_cboxes(self):
        for i in range(1, 5):
            key = f"serial{i}_cbox"
            assert "disabled" in COMBO_BOX_MAPPINGS[key]
            assert "dummy" in COMBO_BOX_MAPPINGS[key]

    def test_keyboard_layout_cbox(self):
        assert "auto" in COMBO_BOX_MAPPINGS["keyboard_layout_cbox"]
        assert "none" in COMBO_BOX_MAPPINGS["keyboard_layout_cbox"]


class TestKeyMappings:
    def test_all_widgets_mapped(self):
        assert KEY_MAPPINGS["fullscreen_sw"] == "fullscreen"
        assert KEY_MAPPINGS["fulldouble_sw"] == "fulldouble"
        assert KEY_MAPPINGS["full_resolution_cbox"] == "fullresolution"
        assert KEY_MAPPINGS["cycles_cbox"] == "cycles"

    def test_key_mappings_count(self):
        assert len(KEY_MAPPINGS) > 20

    def test_key_mappings_includes_autoexec(self):
        assert "autoexec_tbox" in KEY_MAPPINGS
        assert KEY_MAPPINGS["autoexec_tbox"] == "autoexec"


class TestLoadConfig:
    def test_load_config_basic(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "test.conf"
        config_path.write_text(
            "[sdl]\n"
            "fullscreen=true\n"
            "output=opengl\n"
            "[dosbox]\n"
            "machine=vgaonly\n"
            "[render]\n"
            "aspect=true\n"
            "[cpu]\n"
            "core=dynamic\n"
            "[serial]\n"
            "serial1=modem\n"
            "[dos]\n"
            "xms=true\n"
            "[ipx]\n"
            "ipx=true\n"
            "[autoexec]\n"
            "MOUNT C C:\\GAMES\n"
        )

        config.read(str(config_path))
        loaded = load_config(config)

        assert loaded.sdl.fullscreen_sw is True
        assert loaded.sdl.output_cbox == "opengl"
        assert loaded.dosbox.machine_cbox == "vgaonly"
        assert loaded.render.aspect_sw is True
        assert loaded.cpu.core_cbox == "dynamic"
        assert loaded.serial.serial1_cbox == "modem"
        assert loaded.dos.xms_sw is True
        assert loaded.ipx.ipx_sw is True
        assert "MOUNT" in loaded.autoexec.autoexec_tbox

    def test_load_config_missing_sections(self):
        config = DOSBoxConfigParser()
        config.read_string("[sdl]\nfullscreen=true\n")

        loaded = load_config(config)

        assert loaded.sdl.fullscreen_sw is True
        assert loaded.dosbox.machine_cbox == "svga_s3"
        assert loaded.cpu.core_cbox == "auto"

    def test_load_config_empty_parser(self):
        config = DOSBoxConfigParser()

        loaded = load_config(config)

        assert loaded.sdl.fullscreen_sw is False
        assert loaded.dosbox.machine_cbox == "svga_s3"
        assert loaded.render.scaler_cbox == "none"

    def test_load_config_with_autoexec_only(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "test.conf"
        config_path.write_text("[autoexec]\nMOUNT C C:\\DOSGAMES\nC:\ncls\n")

        config.read(str(config_path))
        loaded = load_config(config)

        assert "MOUNT C C:\\DOSGAMES" in loaded.autoexec.autoexec_tbox
        assert "cls" in loaded.autoexec.autoexec_tbox

    def test_load_config_missing_all_optional_sections(self):
        config = DOSBoxConfigParser()
        config.read_string("")

        loaded = load_config(config)

        assert loaded.sdl.full_resolution_cbox == "original"
        assert loaded.dosbox.memsize_spin == 16
        assert loaded.render.frameskip_spin == 0
        assert loaded.serial.serial1_cbox == "disabled"
        assert loaded.dos.xms_sw is True
        assert loaded.ipx.ipx_sw is False

    def test_load_config_partial_sections(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "test.conf"
        config_path.write_text("[sdl]\nfullscreen=true\noutput=opengl\n")

        config.read(str(config_path))
        loaded = load_config(config)

        assert loaded.sdl.fullscreen_sw is True
        assert loaded.sdl.output_cbox == "opengl"
        assert loaded.dosbox.machine_cbox == "svga_s3"
        assert loaded.cpu.core_cbox == "auto"


class TestSoundConfig:
    def test_sound_config_defaults(self):
        config = SoundConfig()
        assert config.sbtype_cbox == "sb16"
        assert config.sb_irq_spin == 7
        assert config.sb_dma_spin == 1

    def test_sound_adv_config_defaults(self):
        config = SoundAdvConfig()
        assert config.sbbase_cbox == "220"
        assert config.sb_hdma_spin == 5
        assert config.sbmixer_sw is True
        assert config.mpu401_cbox == "intelligent"
        assert config.oplmode_cbox == "auto"
        assert config.oplemu_cbox == "default"
        assert config.opl_rate_spin == 44100

    def test_load_config_with_sound_section(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "test.conf"
        config_path.write_text(
            "[sound]\nsbtype=sb16\nirq=5\ndma=3\nsbbase=240\nhdma=6\nsbmixer=true\n"
        )

        config.read(str(config_path))
        loaded = load_config(config)

        assert loaded.sound.sbtype_cbox == "sb16"
        assert loaded.sound.sb_irq_spin == 5
        assert loaded.sound.sb_dma_spin == 3
        assert loaded.sound_adv.sbbase_cbox == "240"
        assert loaded.sound_adv.sb_hdma_spin == 6
        assert loaded.sound_adv.sbmixer_sw is True

    def test_sound_combo_box_mappings(self):
        assert "sbtype_cbox" in COMBO_BOX_MAPPINGS
        assert "sb16" in COMBO_BOX_MAPPINGS["sbtype_cbox"]
        assert "sbpro2" in COMBO_BOX_MAPPINGS["sbtype_cbox"]
        assert "none" in COMBO_BOX_MAPPINGS["sbtype_cbox"]

    def test_sound_key_mappings(self):
        assert KEY_MAPPINGS["sbtype_cbox"] == "sbtype"
        assert KEY_MAPPINGS["sb_irq_spin"] == "irq"
        assert KEY_MAPPINGS["sb_dma_spin"] == "dma"
        assert KEY_MAPPINGS["sbbase_cbox"] == "sbbase"
        assert KEY_MAPPINGS["mpu401_cbox"] == "mpu401"


class TestAdditionalSoundSections:
    def test_mixer_config_defaults(self):
        config = MixerConfig()
        assert config.nosound_sw is False
        assert config.mixer_rate_cbox == "44100"
        assert config.blocksize_cbox == "1024"
        assert config.prebuffer_spin == 25

    def test_midi_config_defaults(self):
        config = MidiConfig()
        assert config.mpu401_cbox == "intelligent"
        assert config.mididevice_cbox == "default"
        assert config.midiconfig_entry == ""

    def test_speaker_config_defaults(self):
        config = SpeakerConfig()
        assert config.pcspeaker_sw is True
        assert config.pcrate_cbox == "44100"
        assert config.tandy_cbox == "auto"
        assert config.tandyrate_cbox == "44100"
        assert config.disney_sw is True

    def test_gus_config_defaults(self):
        config = GusConfig()
        assert config.gus_sw is False
        assert config.gusrate_cbox == "44100"
        assert config.gusbase_cbox == "240"
        assert config.gusirq_spin == 5
        assert config.gusdma_spin == 3
        assert config.ultradir_entry == "C:\\ULTRASND"

    def test_load_config_with_mixer_midi_speaker_gus_sections(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "test.conf"
        config_path.write_text(
            "[mixer]\n"
            "nosound=true\n"
            "rate=22050\n"
            "blocksize=2048\n"
            "prebuffer=50\n"
            "[midi]\n"
            "mpu401=uart\n"
            "mididevice=alsa\n"
            "midiconfig=2\n"
            "[speaker]\n"
            "pcspeaker=false\n"
            "pcrate=22050\n"
            "tandy=on\n"
            "tandyrate=16000\n"
            "disney=false\n"
            "[gus]\n"
            "gus=true\n"
            "gusrate=49716\n"
            "gusbase=260\n"
            "gusirq=9\n"
            "gusdma=6\n"
            "ultradir=C:\\GUS\n"
        )

        config.read(str(config_path))
        loaded = load_config(config)

        assert loaded.mixer.nosound_sw is True
        assert loaded.mixer.mixer_rate_cbox == "22050"
        assert loaded.mixer.blocksize_cbox == "2048"
        assert loaded.mixer.prebuffer_spin == 50
        assert loaded.midi.mpu401_cbox == "uart"
        assert loaded.midi.mididevice_cbox == "alsa"
        assert loaded.midi.midiconfig_entry == "2"
        assert loaded.speaker.pcspeaker_sw is False
        assert loaded.speaker.pcrate_cbox == "22050"
        assert loaded.speaker.tandy_cbox == "on"
        assert loaded.speaker.tandyrate_cbox == "16000"
        assert loaded.speaker.disney_sw is False
        assert loaded.gus.gus_sw is True
        assert loaded.gus.gusrate_cbox == "49716"
        assert loaded.gus.gusbase_cbox == "260"
        assert loaded.gus.gusirq_spin == 9
        assert loaded.gus.gusdma_spin == 6
        assert loaded.gus.ultradir_entry == "C:\\GUS"


class TestJoystickConfig:
    def test_joystick_config_defaults(self):
        config = JoystickConfig()
        assert config.joysticktype_cbox == "auto"
        assert config.autofire_sw is False

    def test_joystick_adv_config_defaults(self):
        config = JoystickAdvConfig()
        assert config.timed_sw is True
        assert config.swap34_sw is False
        assert config.buttonwrap_sw is False
        assert config.joy_x_axis_spin == 0
        assert config.joy_y_axis_spin == 1

    def test_load_config_with_joystick_section(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "test.conf"
        config_path.write_text(
            "[joystick]\njoysticktype=2axis\nautofire=true\ntimed=false\nswap34=true\n"
        )

        config.read(str(config_path))
        loaded = load_config(config)

        assert loaded.joystick.joysticktype_cbox == "2axis"
        assert loaded.joystick.autofire_sw is True
        assert loaded.joystick_adv.timed_sw is False
        assert loaded.joystick_adv.swap34_sw is True

    def test_joystick_combo_box_mappings(self):
        assert "joysticktype_cbox" in COMBO_BOX_MAPPINGS
        assert "auto" in COMBO_BOX_MAPPINGS["joysticktype_cbox"]
        assert "2axis" in COMBO_BOX_MAPPINGS["joysticktype_cbox"]
        assert "4axis" in COMBO_BOX_MAPPINGS["joysticktype_cbox"]

    def test_joystick_key_mappings(self):
        assert KEY_MAPPINGS["joysticktype_cbox"] == "joysticktype"
        assert KEY_MAPPINGS["autofire_sw"] == "autofire"
        assert KEY_MAPPINGS["timed_sw"] == "timed"
        assert KEY_MAPPINGS["swap34_sw"] == "swap34"
        assert KEY_MAPPINGS["buttonwrap_sw"] == "buttonwrap"
