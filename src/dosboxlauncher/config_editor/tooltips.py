"""Tooltip text for DOSBox configuration editor widgets.

Tooltips are extracted from the DOSBox base-config.conf comments.
Each entry maps a widget ID to its help text.
"""

# SDL (Display) section tooltips
TOOLTIPS = {
    # SDL Tab
    "fullscreen_sw": "Start DOSBox directly in fullscreen mode. Press ALT-Enter to toggle.",
    "fulldouble_sw": "Use double buffering in fullscreen. Can reduce flickering but may slow performance.",
    "full_resolution_cbox": "Resolution to use for fullscreen: 'original' uses game resolution, 'desktop' uses your monitor's native resolution, or specify fixed size like 1024x768.",
    "wind_res_cbox": "Scale the window to this size if the output device supports hardware scaling. surface output does not support this.",
    "output_cbox": "Video system to use for output. Options: surface (default), overlay, opengl, openglnb.",
    "autolock_sw": "Mouse will automatically lock to the DOSBox window when you click. Press CTRL-F10 to unlock.",
    "sensitivity_spin": "Mouse sensitivity adjustment. Lower values reduce sensitivity, higher values increase it.",
    "wait_on_error_sw": "Wait before closing the console window if DOSBox encounters an error. Useful for reading error messages.",
    "priority_cbox": "Priority levels for DOSBox. Second value (after comma) is for when DOSBox is not focused/minimized. Options: lowest, lower, normal, higher, highest, pause.",
    "mapper_file_entry": "File used to load/save key/event mappings. Resetmapper only works with the default value.",
    "use_scan_codes_sw": "Avoid usage of symbolic keys. Might not work on all operating systems.",
    # DOSBox Tab
    "language_entry": "Select a different language file for DOSBox messages and texts.",
    "machine_cbox": "Type of machine DOSBox tries to emulate. Options: hercules, cga, tandy, pcjr, ega, vgaonly, svga_s3, svga_et3000, svga_et4000, svga_paradise, vesa_nofb, vesa_oldvbe.",
    "captures_entry": "Directory where wave, midi, and screenshot files get captured.",
    "memsize_spin": "Amount of memory DOSBox has in megabytes. Leave at default to avoid problems with some games.",
    # Render Tab
    "frameskip_spin": "How many frames DOSBox skips before drawing one. Increase to improve performance on slow systems.",
    "aspect_sw": "Enable aspect ratio correction. Prevents stretching on wide monitors but can slow rendering.",
    "scaler_cbox": "Scaler used to enlarge low resolution modes. Options: none, normal2x, normal3x, advmame2x, advmame3x, hq2x, hq3x, 2xsai, super2xsai, supereagle, tv2x, tv3x, rgb2x, rgb3x, scan2x, scan3x.",
    # CPU Tab
    "core_cbox": "CPU core used in emulation. 'auto' switches to dynamic if available. Options: auto, dynamic, normal, simple.",
    "cpu_type_cbox": "CPU type to emulate. 'auto' is fastest. Options: auto, 386, 386_slow, 486_slow, pentium_slow, 386_prefetch.",
    "cycles_cbox": "Instructions DOSBox tries to emulate each millisecond. 'auto' guesses what games need. 'fixed 4000' sets specific cycles. 'max' uses maximum.",
    "cycle_up_spin": "Amount of cycles to increase with CTRL-F12 key combo.",
    "cycle_down_spin": "Amount of cycles to decrease with CTRL-F11 key combo. Values below 100 are treated as percentage.",
    # Serial Tab
    "serial1_cbox": "Type of device connected to COM1. Options: dummy, disabled, modem, nullmodem, directserial.",
    "serial2_cbox": "Type of device connected to COM2. Options: dummy, disabled, modem, nullmodem, directserial.",
    "serial3_cbox": "Type of device connected to COM3. Options: dummy, disabled, modem, nullmodem, directserial.",
    "serial4_cbox": "Type of device connected to COM4. Options: dummy, disabled, modem, nullmodem, directserial.",
    # DOS Tab
    "xms_sw": "Enable XMS (Extended Memory Specification) support.",
    "ems_sw": "Enable EMS (Expanded Memory Specification) support.",
    "umb_sw": "Enable Upper Memory Blocks support.",
    "keyboard_layout_cbox": "Language code for keyboard layout (e.g., us, uk, gr). 'auto' attempts to detect.",
    # IPX Tab
    "ipx_sw": "Enable IPX over UDP/IP emulation for networked games.",
    # Autoexec Tab
    "autoexec_tbox": "Commands to run at DOSBox startup. Use MOUNT commands to mount game directories.",
    # Sound Tab (Basic)
    "sbtype_cbox": "Type of Sound Blaster to emulate. Options: sb1, sb2, sb2.0, sb3, sbpro1, sbpro2, sb16, sb16vibra, sb16ul, gus, pas16, none.",
    "sb_irq_spin": "IRQ number of the Sound Blaster. Common values: 7, 5, 3, 9, 10, 11, 12.",
    "sb_dma_spin": "DMA channel for the Sound Blaster. Common values: 1, 5, 0, 3, 6, 7.",
    # Sound Advanced
    "sbbase_cbox": "I/O base address of the Sound Blaster. Options: 220, 240, 260, 280, 2a0, 2c0, 2e0, 300.",
    "sb_hdma_spin": "High DMA channel for Sound Blaster. Common values: 1, 5, 0, 3, 6, 7.",
    "sbmixer_sw": "Allow the Sound Blaster mixer to modify the DOSBox mixer settings.",
    "mpu401_cbox": "Type of MPU-401 to emulate. 'intelligent' is recommended. Options: intelligent, uart, none.",
    "oplmode_cbox": "Type of OPL emulation. 'auto' determines mode based on Sound Blaster type. Options: auto, cms, dbopl, al, none.",
    "oplemu_cbox": "Provider for OPL emulation. 'compat' may provide better quality. Options: default, compat, fast, none.",
    "opl_rate_spin": "Sample rate of OPL music emulation. Use 49716 for highest quality.",
    # Mixer
    "nosound_sw": "Enable silent mode. Sound is still emulated internally, but nothing is played.",
    "mixer_rate_cbox": "Mixer sample rate. Setting device rates higher than this can reduce sound quality.",
    "blocksize_cbox": "Mixer block size. Larger blocks may reduce stutter but increase audio lag.",
    "prebuffer_spin": "How many milliseconds of audio data to keep buffered beyond the block size.",
    # MIDI
    "mididevice_cbox": "Device that receives MIDI data from MPU-401. Choices depend on your platform and setup.",
    "midiconfig_entry": "Special configuration for the MIDI device, often a device id or soundfont path.",
    # Speaker
    "pcspeaker_sw": "Enable PC speaker emulation.",
    "pcrate_cbox": "Sample rate used for PC speaker sound generation.",
    "tandy_cbox": "Enable Tandy sound emulation. 'auto' only enables it when the machine type is Tandy.",
    "tandyrate_cbox": "Sample rate used for Tandy 3-voice sound generation.",
    "disney_sw": "Enable Disney Sound Source emulation, compatible with Covox-style speech devices.",
    # Gravis Ultrasound
    "gus_sw": "Enable Gravis Ultrasound emulation.",
    "gusrate_cbox": "Sample rate used for Ultrasound emulation.",
    "gusbase_cbox": "I/O base address of the Gravis Ultrasound.",
    "gusirq_spin": "IRQ number used by the Gravis Ultrasound emulation.",
    "gusdma_spin": "DMA channel used by the Gravis Ultrasound emulation.",
    "ultradir_entry": "Path to the Ultrasound directory containing the required MIDI patch files.",
    # Joystick Tab (Basic)
    "joysticktype_cbox": "Type of joystick to emulate. 'auto' chooses based on detected joystick. Options: auto, none, 2axis, 4axis, fcs, ch, cross, wingman, wingman-fc, sidewinder, gamepadpro, grip, grip4, stick, stingray, snac.",
    "autofire_sw": "Continuously fires as long as you keep the button pressed.",
    # Joystick Advanced
    "timed_sw": "Enable timed intervals for axis. Enable if joystick drifts unexpectedly.",
    "swap34_sw": "Swap the 3rd and 4th axis. Useful for certain joystick configurations.",
    "buttonwrap_sw": "Enable button wrapping at the number of emulated buttons.",
    "joy_x_axis_spin": "Which axis to use for X (horizontal) axis. Usually 0.",
    "joy_y_axis_spin": "Which axis to use for Y (vertical) axis. Usually 1.",
}
