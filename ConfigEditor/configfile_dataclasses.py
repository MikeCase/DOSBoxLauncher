from dataclasses import dataclass, field
from typing import List

@dataclass
class SDLConfig:
    fullscreen_sw: bool
    fulldouble_sw: bool
    full_resolution_cbox: str
    wind_res_cbox: str
    output_cbox: str
    autolock_sw: bool
    sensitivity_spin: int
    wait_on_error_sw: bool
    priority_cbox: str
    mapper_file_entry: str
    use_scan_codes_sw: bool

@dataclass
class DosboxConfig:
    language_entry: str
    machine_cbox: str
    captures_entry: str
    memsize_spin: int

@dataclass
class RenderConfig:
    frameskip_spin: int
    aspect_sw: bool
    scaler_cbox: str

@dataclass
class CPUConfig:
    core_cbox: str
    cpu_type_cbox: str
    cycles_cbox: str
    cycle_up_spin: int
    cycle_down_spin: int

@dataclass
class SerialConfig:
    serial1_cbox: str
    serial2_cbox: str
    serial3_cbox: str
    serial4_cbox: str


@dataclass
class DosConfig:
    xms_sw: bool
    ems_sw: bool
    umb_sw: bool
    keyboard_layout_cbox: str

@dataclass
class IpxConfig:
    ipx_sw: bool

@dataclass
class AutoExecConfig:
    autoexec_tbox: str

@dataclass
class Config:
    sdl: SDLConfig
    dosbox: DosboxConfig
    render: RenderConfig
    cpu: CPUConfig
    serial: SerialConfig
    dos: DosConfig
    ipx: IpxConfig
    autoexec: AutoExecConfig



@dataclass
class ComboBoxMappings:
    full_resolution_cbox: List[str] = field(default_factory=lambda: ["original", "640x480", "800x600", "1024x768", "1280x720", "1920x1024"])
    wind_res_cbox: List[str] = field(default_factory=lambda: ["original", "640x480", "800x600", "1024x768", "1280x720", "1920x1024"])
    output_cbox: List[str] = field(default_factory=lambda: ["surface", "overlay", "opengl", "ddraw"])
    priority_cbox: List[str] = field(default_factory=lambda: ['higher, normal'])
    machine_cbox: List[str] = field(default_factory=lambda: ['hercules', 'cga', 'tandy', 'pcjr', 'ega', 'vgaonly', 'svga_s3', 'svga_et3000', 'svga_et4000', 'svga_paradise', 'vesa_nofb', 'vesa_oldvbe'])
    scaler_cbox: List[str] = field(default_factory=lambda: ['none', 'normal2x', 'normal3x', 'tv2x', 'tv3x', 'rgb3x', 'rgb2x', 'scan2x', 'scan3x', 'advmame2x', 'advmame3x', 'advinterp2x', 'advinterp3x', '2xsai', 'super2xsai', 'supereagle', 'hq2x', 'hq3x'])
    core_cbox: List[str] = field(default_factory=lambda: ['simple', 'normal', 'dynamic', 'auto'])
    cpu_type_cbox: List[str] = field(default_factory=lambda: ['auto', '386', '486_slow', 'pentium_slow', '386_prefetch'])
    cycles_cbox: List[str] = field(default_factory=lambda: ['fixed 5000, cycles=5000', 'max', 'max limit 50000', 'max 50%', 'auto', 'auto 5000 50% limit 50000'])
    serial1_cbox: List[str] = field(default_factory=lambda: ['dummy', 'modem', 'nullmodem', 'directserial', 'disabled'])
    serial2_cbox: List[str] = field(default_factory=lambda: ['dummy', 'modem', 'nullmodem', 'directserial', 'disabled'])
    serial3_cbox: List[str] = field(default_factory=lambda: ['dummy', 'modem', 'nullmodem', 'directserial', 'disabled'])
    serial4_cbox: List[str] = field(default_factory=lambda: ['dummy', 'modem', 'nullmodem', 'directserial', 'disabled'])
    keyboard_layout_cbox: List[str] = field(default_factory=lambda: ['auto', 'none'])

# Define all your key mappings in a central place
KEY_MAPPINGS = {
            'fullscreen_sw': 'fullscreen',
            'fulldouble_sw': 'fulldouble',
            'full_resolution_cbox': 'fullresolution',
            'wind_res_cbox': 'windowresolution',
            'output_cbox': 'output',
            'autolock_sw': 'autolock',
            'sensitivity_spin': 'sensitivity',
            'wait_on_error_sw': 'waitonerror',
            'priority_cbox': 'priority',
            'mapper_file_entry': 'mapperfile',
            'use_scan_codes_sw': 'usescancodes',
            'language_entry': 'language',
            'memsize_spin': 'memsize',
            'machine_cbox': 'machine',
            'captures_entry': 'captures',
            'frameskip_spin': 'frameskip',
            'aspect_sw': 'aspect',
            'scaler_cbox': 'scaler',
            'core_cbox': 'core',
            'cpu_type_cbox': 'cputype',
            'cycles_cbox': 'cycles',
            'cycle_up_spin': 'cycleup',
            'cycle_down_spin': 'cycledown',
            'serial1_cbox': 'serial1',
            'serial2_cbox': 'serial2',
            'serial3_cbox': 'serial3',
            'serial4_cbox': 'serial4',
            'xms_sw': 'xms',
            'ems_sw': 'ems',
            'umb_sw': 'umb',
            'keyboard_layout_cbox': 'keyboardlayout',
            'ipx_sw': 'ipx',
            'autoexec_tbox': 'autoexec'  # Special case for autoexec
        }

def load_config(config):
        return Config(
                sdl=SDLConfig(
                    fullscreen_sw=config['sdl'].getboolean('fullscreen'),
                    fulldouble_sw=config['sdl'].getboolean('fulldouble'),
                    full_resolution_cbox=config['sdl']['fullresolution'],
                    wind_res_cbox=config['sdl']['windowresolution'],
                    output_cbox=config['sdl']['output'],
                    autolock_sw=config['sdl'].getboolean('autolock'),
                    sensitivity_spin=config['sdl'].getint('sensitivity'),
                    wait_on_error_sw=config['sdl'].getboolean('waitonerror'),
                    priority_cbox=config['sdl']['priority'],
                    mapper_file_entry=config['sdl']['mapperfile'],
                    use_scan_codes_sw=config['sdl'].getboolean('usescancodes'),
                ),
                dosbox=DosboxConfig(
                    language_entry=config['dosbox']['language'],
                    machine_cbox=config['dosbox']['machine'],
                    captures_entry=config['dosbox']['captures'],
                    memsize_spin=config['dosbox'].getint('memsize'),
                ),
                render=RenderConfig(
                    frameskip_spin=config['render'].getint('frameskip'),
                    aspect_sw=config['render'].getboolean('aspect'),
                    scaler_cbox=config['render']['scaler'],
                ),
                cpu=CPUConfig(
                    core_cbox=config['cpu']['core'],
                    cpu_type_cbox=config['cpu']['cputype'],
                    cycles_cbox=config['cpu']['cycles'],
                    cycle_up_spin=config['cpu'].getint('cycleup'),
                    cycle_down_spin=config['cpu'].getint('cycledown'),
                ),
                serial=SerialConfig(
                    serial1_cbox=config['serial']['serial1'],
                    serial2_cbox=config['serial']['serial2'],
                    serial3_cbox=config['serial']['serial3'],
                    serial4_cbox=config['serial']['serial4'],
                ),
                dos=DosConfig(
                    xms_sw=config['dos'].getboolean('xms'),
                    ems_sw=config['dos'].getboolean('ems'),
                    umb_sw=config['dos'].getboolean('umb'),
                    keyboard_layout_cbox=config['dos']['keyboardlayout'],
                ),
                ipx=IpxConfig(
                    ipx_sw=config['ipx'].getboolean('ipx'),
                ),
                autoexec=AutoExecConfig(
                    autoexec_tbox=config.get_raw_section('autoexec'),
                )
            )