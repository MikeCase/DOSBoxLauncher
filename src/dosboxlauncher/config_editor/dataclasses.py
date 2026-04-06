"""Data classes for DOSBox configuration file parsing."""

from __future__ import annotations

import configparser
from dataclasses import dataclass, field

from .parser import DOSBoxConfigParser

# Dataclasses for each DOSBox config section
# Each maps to a [section] in the .conf file


@dataclass
class SDLConfig:
    """SDL display settings."""

    fullscreen_sw: bool = False
    fulldouble_sw: bool = False
    full_resolution_cbox: str = "original"
    wind_res_cbox: str = "original"
    output_cbox: str = "surface"
    autolock_sw: bool = True
    sensitivity_spin: int = 1
    wait_on_error_sw: bool = True
    priority_cbox: str = "higher,normal"
    mapper_file_entry: str = ""
    use_scan_codes_sw: bool = False


@dataclass
class DosboxConfig:
    """Core DOSBox settings."""

    language_entry: str = ""
    machine_cbox: str = "svga_s3"
    captures_entry: str = ""
    memsize_spin: int = 16


@dataclass
class RenderConfig:
    """Video rendering settings."""

    frameskip_spin: int = 0
    aspect_sw: bool = False
    scaler_cbox: str = "none"


@dataclass
class CPUConfig:
    """CPU emulation settings."""

    core_cbox: str = "auto"
    cpu_type_cbox: str = "auto"
    cycles_cbox: str = "auto"
    cycle_up_spin: int = 10
    cycle_down_spin: int = 10


@dataclass
class SerialConfig:
    """Serial port settings."""

    serial1_cbox: str = "disabled"
    serial2_cbox: str = "disabled"
    serial3_cbox: str = "disabled"
    serial4_cbox: str = "disabled"


@dataclass
class DosConfig:
    """DOS emulation settings."""

    xms_sw: bool = True
    ems_sw: bool = True
    umb_sw: bool = True
    keyboard_layout_cbox: str = "auto"


@dataclass
class IpxConfig:
    """IPX networking settings."""

    ipx_sw: bool = False


@dataclass
class AutoExecConfig:
    """Autoexec section - raw commands executed at DOSBox startup."""

    autoexec_tbox: str = ""


@dataclass
class SoundConfig:
    """Basic sound settings - Sound Blaster and MIDI."""

    sbtype_cbox: str = "sb16"
    sb_irq_spin: int = 7
    sb_dma_spin: int = 1


@dataclass
class SoundAdvConfig:
    """Advanced sound settings."""

    sbbase_cbox: str = "220"
    sb_hdma_spin: int = 5
    sbmixer_sw: bool = True
    mpu401_cbox: str = "intelligent"
    oplmode_cbox: str = "auto"
    oplemu_cbox: str = "default"
    opl_rate_spin: int = 44100


@dataclass
class MixerConfig:
    """Mixer settings."""

    nosound_sw: bool = False
    mixer_rate_cbox: str = "44100"
    blocksize_cbox: str = "1024"
    prebuffer_spin: int = 25


@dataclass
class MidiConfig:
    """MIDI settings."""

    mpu401_cbox: str = "intelligent"
    mididevice_cbox: str = "default"
    midiconfig_entry: str = ""


@dataclass
class SpeakerConfig:
    """PC speaker and Tandy settings."""

    pcspeaker_sw: bool = True
    pcrate_cbox: str = "44100"
    tandy_cbox: str = "auto"
    tandyrate_cbox: str = "44100"
    disney_sw: bool = True


@dataclass
class GusConfig:
    """Gravis Ultrasound settings."""

    gus_sw: bool = False
    gusrate_cbox: str = "44100"
    gusbase_cbox: str = "240"
    gusirq_spin: int = 5
    gusdma_spin: int = 3
    ultradir_entry: str = r"C:\ULTRASND"


@dataclass
class JoystickConfig:
    """Basic joystick settings."""

    joysticktype_cbox: str = "auto"
    autofire_sw: bool = False


@dataclass
class JoystickAdvConfig:
    """Advanced joystick settings."""

    timed_sw: bool = True
    swap34_sw: bool = False
    buttonwrap_sw: bool = False
    joy_x_axis_spin: int = 0
    joy_y_axis_spin: int = 1


@dataclass
class Config:
    """Container for all DOSBox config sections."""

    sdl: SDLConfig = field(default_factory=SDLConfig)
    dosbox: DosboxConfig = field(default_factory=DosboxConfig)
    render: RenderConfig = field(default_factory=RenderConfig)
    cpu: CPUConfig = field(default_factory=CPUConfig)
    serial: SerialConfig = field(default_factory=SerialConfig)
    dos: DosConfig = field(default_factory=DosConfig)
    ipx: IpxConfig = field(default_factory=IpxConfig)
    autoexec: AutoExecConfig = field(default_factory=AutoExecConfig)
    sound: SoundConfig = field(default_factory=SoundConfig)
    sound_adv: SoundAdvConfig = field(default_factory=SoundAdvConfig)
    mixer: MixerConfig = field(default_factory=MixerConfig)
    midi: MidiConfig = field(default_factory=MidiConfig)
    speaker: SpeakerConfig = field(default_factory=SpeakerConfig)
    gus: GusConfig = field(default_factory=GusConfig)
    joystick: JoystickConfig = field(default_factory=JoystickConfig)
    joystick_adv: JoystickAdvConfig = field(default_factory=JoystickAdvConfig)


# Valid options for ComboBox dropdowns in the UI
COMBO_BOX_MAPPINGS = {
    "full_resolution_cbox": ["original", "640x480", "800x600", "1024x768", "1280x720", "1920x1024"],
    "wind_res_cbox": ["original", "640x480", "800x600", "1024x768", "1280x720", "1920x1024"],
    "output_cbox": ["surface", "overlay", "opengl", "ddraw"],
    "priority_cbox": ["higher,normal"],
    "machine_cbox": [
        "hercules",
        "cga",
        "tandy",
        "pcjr",
        "ega",
        "vgaonly",
        "svga_s3",
        "svga_et3000",
        "svga_et4000",
        "svga_paradise",
        "vesa_nofb",
        "vesa_oldvbe",
    ],
    "scaler_cbox": [
        "none",
        "normal2x",
        "normal3x",
        "tv2x",
        "tv3x",
        "rgb3x",
        "rgb2x",
        "scan2x",
        "scan3x",
        "advmame2x",
        "advmame3x",
        "advinterp2x",
        "advinterp3x",
        "2xsai",
        "super2xsai",
        "supereagle",
        "hq2x",
        "hq3x",
    ],
    "core_cbox": ["simple", "normal", "dynamic", "auto"],
    "cpu_type_cbox": ["auto", "386", "486_slow", "pentium_slow", "386_prefetch"],
    "cycles_cbox": [
        "fixed 5000",
        "max",
        "max limit 50000",
        "max 50%",
        "auto",
        "auto 5000 50% limit 50000",
    ],
    "serial1_cbox": ["dummy", "modem", "nullmodem", "directserial", "disabled"],
    "serial2_cbox": ["dummy", "modem", "nullmodem", "directserial", "disabled"],
    "serial3_cbox": ["dummy", "modem", "nullmodem", "directserial", "disabled"],
    "serial4_cbox": ["dummy", "modem", "nullmodem", "directserial", "disabled"],
    "keyboard_layout_cbox": ["auto", "none"],
    "sbtype_cbox": [
        "sb1",
        "sb2",
        "sb2.0",
        "sb3",
        "sbpro1",
        "sbpro2",
        "sb16",
        "sb16vibra",
        "sb envy24",
        "sb envy24ht",
        "sb16ul",
        "gus",
        "pas16",
        "realtime",
        "none",
    ],
    "sbbase_cbox": ["220", "240", "260", "280", "2a0", "2c0", "2e0", "300", "320", "340", "360"],
    "mixer_rate_cbox": ["44100", "48000", "32000", "22050", "16000", "11025", "8000", "49716"],
    "blocksize_cbox": ["1024", "2048", "4096", "8192", "512", "256"],
    "mpu401_cbox": ["intelligent", "uart", "none"],
    "mididevice_cbox": ["default", "win32", "alsa", "oss", "coreaudio", "coremidi", "none"],
    "oplmode_cbox": ["auto", "cms", "dbopl", "al", "none"],
    "oplemu_cbox": ["default", "compat", "fast", "none"],
    "pcrate_cbox": ["44100", "48000", "32000", "22050", "16000", "11025", "8000", "49716"],
    "tandy_cbox": ["auto", "on", "off"],
    "tandyrate_cbox": ["44100", "48000", "32000", "22050", "16000", "11025", "8000", "49716"],
    "gusrate_cbox": ["44100", "48000", "32000", "22050", "16000", "11025", "8000", "49716"],
    "gusbase_cbox": ["240", "220", "260", "280", "2a0", "2c0", "2e0", "300"],
    "joysticktype_cbox": [
        "auto",
        "none",
        "2axis",
        "4axis_2",
        "4axis",
        "fcs",
        "ch",
        "cross",
        "wingman",
        "wingman-fc",
        "sidewinder",
        "gamepadpro",
        "grip",
        "grip4",
        "stick",
        "stingray",
        "snac",
    ],
}

# Maps UI widget names to DOSBox config keys
KEY_MAPPINGS = {
    "fullscreen_sw": "fullscreen",
    "fulldouble_sw": "fulldouble",
    "full_resolution_cbox": "fullresolution",
    "wind_res_cbox": "windowresolution",
    "output_cbox": "output",
    "autolock_sw": "autolock",
    "sensitivity_spin": "sensitivity",
    "wait_on_error_sw": "waitonerror",
    "priority_cbox": "priority",
    "mapper_file_entry": "mapperfile",
    "use_scan_codes_sw": "usescancodes",
    "language_entry": "language",
    "memsize_spin": "memsize",
    "machine_cbox": "machine",
    "captures_entry": "captures",
    "frameskip_spin": "frameskip",
    "aspect_sw": "aspect",
    "scaler_cbox": "scaler",
    "core_cbox": "core",
    "cpu_type_cbox": "cputype",
    "cycles_cbox": "cycles",
    "cycle_up_spin": "cycleup",
    "cycle_down_spin": "cycledown",
    "serial1_cbox": "serial1",
    "serial2_cbox": "serial2",
    "serial3_cbox": "serial3",
    "serial4_cbox": "serial4",
    "xms_sw": "xms",
    "ems_sw": "ems",
    "umb_sw": "umb",
    "keyboard_layout_cbox": "keyboardlayout",
    "ipx_sw": "ipx",
    "autoexec_tbox": "autoexec",
    # Sound config (basic)
    "sbtype_cbox": "sbtype",
    "sb_irq_spin": "irq",
    "sb_dma_spin": "dma",
    # Sound config (advanced)
    "sbbase_cbox": "sbbase",
    "sb_hdma_spin": "hdma",
    "sbmixer_sw": "sbmixer",
    "mpu401_cbox": "mpu401",
    "oplmode_cbox": "oplmode",
    "oplemu_cbox": "oplemu",
    "opl_rate_spin": "oplrate",
    "nosound_sw": "nosound",
    "mixer_rate_cbox": "rate",
    "blocksize_cbox": "blocksize",
    "prebuffer_spin": "prebuffer",
    "mididevice_cbox": "mididevice",
    "midiconfig_entry": "midiconfig",
    "pcspeaker_sw": "pcspeaker",
    "pcrate_cbox": "pcrate",
    "tandy_cbox": "tandy",
    "tandyrate_cbox": "tandyrate",
    "disney_sw": "disney",
    "gus_sw": "gus",
    "gusrate_cbox": "gusrate",
    "gusbase_cbox": "gusbase",
    "gusirq_spin": "gusirq",
    "gusdma_spin": "gusdma",
    "ultradir_entry": "ultradir",
    # Joystick config (basic)
    "joysticktype_cbox": "joysticktype",
    "autofire_sw": "autofire",
    # Joystick config (advanced)
    "timed_sw": "timed",
    "swap34_sw": "swap34",
    "buttonwrap_sw": "buttonwrap",
    "joy_x_axis_spin": "joy_xAxis",
    "joy_y_axis_spin": "joy_yAxis",
}


SECTION_MAPPINGS = {
    "sound": "sblaster",
    "sound_adv": "sblaster",
}


def _get_section(config: DOSBoxConfigParser, *names: str):
    """Return the first matching config section."""
    for name in names:
        try:
            return config[name]
        except KeyError:
            continue
    raise KeyError(names[0])


def load_config(config: DOSBoxConfigParser) -> Config:
    """Load configuration from a DOSBoxConfigParser instance.

    Uses defaults if config sections are missing.
    """
    # SDL section
    try:
        sdl = SDLConfig(
            fullscreen_sw=config["sdl"].getboolean("fullscreen"),
            fulldouble_sw=config["sdl"].getboolean("fulldouble"),
            full_resolution_cbox=config["sdl"].get("fullresolution"),
            wind_res_cbox=config["sdl"].get("windowresolution"),
            output_cbox=config["sdl"].get("output"),
            autolock_sw=config["sdl"].getboolean("autolock"),
            sensitivity_spin=config["sdl"].getint("sensitivity"),
            wait_on_error_sw=config["sdl"].getboolean("waitonerror"),
            priority_cbox=config["sdl"].get("priority"),
            mapper_file_entry=config["sdl"].get("mapperfile"),
            use_scan_codes_sw=config["sdl"].getboolean("usescancodes"),
        )
    except (configparser.NoSectionError, KeyError):
        sdl = SDLConfig()

    # DOSBox section
    try:
        dosbox = DosboxConfig(
            language_entry=config["dosbox"].get("language"),
            machine_cbox=config["dosbox"].get("machine"),
            captures_entry=config["dosbox"].get("captures"),
            memsize_spin=config["dosbox"].getint("memsize"),
        )
    except (configparser.NoSectionError, KeyError):
        dosbox = DosboxConfig()

    # Render section
    try:
        render = RenderConfig(
            frameskip_spin=config["render"].getint("frameskip"),
            aspect_sw=config["render"].getboolean("aspect"),
            scaler_cbox=config["render"].get("scaler"),
        )
    except (configparser.NoSectionError, KeyError):
        render = RenderConfig()

    # CPU section
    try:
        cpu = CPUConfig(
            core_cbox=config["cpu"].get("core"),
            cpu_type_cbox=config["cpu"].get("cputype"),
            cycles_cbox=config["cpu"].get("cycles"),
            cycle_up_spin=config["cpu"].getint("cycleup"),
            cycle_down_spin=config["cpu"].getint("cycledown"),
        )
    except (configparser.NoSectionError, KeyError):
        cpu = CPUConfig()

    # Serial section
    try:
        serial = SerialConfig(
            serial1_cbox=config["serial"].get("serial1"),
            serial2_cbox=config["serial"].get("serial2"),
            serial3_cbox=config["serial"].get("serial3"),
            serial4_cbox=config["serial"].get("serial4"),
        )
    except (configparser.NoSectionError, KeyError):
        serial = SerialConfig()

    # DOS section
    try:
        dos = DosConfig(
            xms_sw=config["dos"].getboolean("xms"),
            ems_sw=config["dos"].getboolean("ems"),
            umb_sw=config["dos"].getboolean("umb"),
            keyboard_layout_cbox=config["dos"].get("keyboardlayout"),
        )
    except (configparser.NoSectionError, KeyError):
        dos = DosConfig()

    # IPX section
    try:
        ipx = IpxConfig(
            ipx_sw=config["ipx"].getboolean("ipx"),
        )
    except (configparser.NoSectionError, KeyError):
        ipx = IpxConfig()

    # Autoexec - uses raw section (not parsed as key-value pairs)
    autoexec = AutoExecConfig(
        autoexec_tbox=config.get_raw_section("autoexec"),
    )

    # Sound section (basic)
    try:
        sblaster = _get_section(config, "sblaster", "sound")
        sound = SoundConfig(
            sbtype_cbox=sblaster.get("sbtype"),
            sb_irq_spin=sblaster.getint("irq"),
            sb_dma_spin=sblaster.getint("dma"),
        )
    except (configparser.NoSectionError, KeyError):
        sound = SoundConfig()

    # Sound section (advanced)
    try:
        sblaster = _get_section(config, "sblaster", "sound")
        sound_adv = SoundAdvConfig(
            sbbase_cbox=sblaster.get("sbbase"),
            sb_hdma_spin=sblaster.getint("hdma"),
            sbmixer_sw=sblaster.getboolean("sbmixer"),
            mpu401_cbox=_get_section(config, "midi", "sblaster", "sound").get("mpu401"),
            oplmode_cbox=sblaster.get("oplmode"),
            oplemu_cbox=sblaster.get("oplemu"),
            opl_rate_spin=sblaster.getint("oplrate"),
        )
    except (configparser.NoSectionError, KeyError):
        sound_adv = SoundAdvConfig()

    try:
        mixer = MixerConfig(
            nosound_sw=config["mixer"].getboolean("nosound"),
            mixer_rate_cbox=config["mixer"].get("rate"),
            blocksize_cbox=config["mixer"].get("blocksize"),
            prebuffer_spin=config["mixer"].getint("prebuffer"),
        )
    except (configparser.NoSectionError, KeyError):
        mixer = MixerConfig()

    try:
        midi = MidiConfig(
            mpu401_cbox=_get_section(config, "midi", "sblaster", "sound").get("mpu401"),
            mididevice_cbox=_get_section(config, "midi").get("mididevice"),
            midiconfig_entry=_get_section(config, "midi").get("midiconfig"),
        )
    except (configparser.NoSectionError, KeyError):
        midi = MidiConfig()

    try:
        speaker = SpeakerConfig(
            pcspeaker_sw=config["speaker"].getboolean("pcspeaker"),
            pcrate_cbox=config["speaker"].get("pcrate"),
            tandy_cbox=config["speaker"].get("tandy"),
            tandyrate_cbox=config["speaker"].get("tandyrate"),
            disney_sw=config["speaker"].getboolean("disney"),
        )
    except (configparser.NoSectionError, KeyError):
        speaker = SpeakerConfig()

    try:
        gus = GusConfig(
            gus_sw=config["gus"].getboolean("gus"),
            gusrate_cbox=config["gus"].get("gusrate"),
            gusbase_cbox=config["gus"].get("gusbase"),
            gusirq_spin=config["gus"].getint("gusirq"),
            gusdma_spin=config["gus"].getint("gusdma"),
            ultradir_entry=config["gus"].get("ultradir"),
        )
    except (configparser.NoSectionError, KeyError):
        gus = GusConfig()

    # Joystick section (basic)
    try:
        joystick = JoystickConfig(
            joysticktype_cbox=config["joystick"].get("joysticktype"),
            autofire_sw=config["joystick"].getboolean("autofire"),
        )
    except (configparser.NoSectionError, KeyError):
        joystick = JoystickConfig()

    # Joystick section (advanced)
    try:
        joystick_adv = JoystickAdvConfig(
            timed_sw=config["joystick"].getboolean("timed"),
            swap34_sw=config["joystick"].getboolean("swap34"),
            buttonwrap_sw=config["joystick"].getboolean("buttonwrap"),
            joy_x_axis_spin=config["joystick"].getint("joy_xAxis"),
            joy_y_axis_spin=config["joystick"].getint("joy_yAxis"),
        )
    except (configparser.NoSectionError, KeyError):
        joystick_adv = JoystickAdvConfig()

    return Config(
        sdl=sdl,
        dosbox=dosbox,
        render=render,
        cpu=cpu,
        serial=serial,
        dos=dos,
        ipx=ipx,
        autoexec=autoexec,
        sound=sound,
        sound_adv=sound_adv,
        mixer=mixer,
        midi=midi,
        speaker=speaker,
        gus=gus,
        joystick=joystick,
        joystick_adv=joystick_adv,
    )
