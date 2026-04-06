"""Config parser for DOSBox configuration files."""

import configparser


class DOSBoxConfigParser(configparser.ConfigParser):
    """Custom ConfigParser that preserves raw sections like autoexec.

    Standard ConfigParser treats everything as key=value pairs.
    DOSBox's autoexec section contains raw commands (like MOUNT, C:).
    This subclass preserves those as raw lines instead of trying to parse them.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._raw_sections: dict[str, list[str]] = {}

    def read(self, filename: str) -> list[str]:
        """Read and parse a DOSBox config file."""
        try:
            with open(filename) as f:
                lines = f.readlines()
        except FileNotFoundError:
            return []

        current_section: str | None = None
        for line in lines:
            line = line.rstrip("\n")
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
                if current_section not in self._raw_sections:
                    self._raw_sections[current_section] = []
            elif current_section and "=" not in line.strip():
                # No "=" - this is a raw command line, not key=value
                self._raw_sections[current_section].append(line)
            else:
                # Has "=" - parse as key=value
                section_content = f"[{current_section}]\n{line}" if current_section else line
                super().read_string(section_content)

        return [filename]

    def get_raw_section(self, section: str) -> str:
        """Get raw section content without parsing as key-value pairs."""
        return "\n".join(self._raw_sections.get(section, []))

    def set_raw_section(self, section: str, content: str | list[str]) -> None:
        """Set raw section content."""
        if isinstance(content, str):
            content = content.splitlines()
        self._raw_sections[section] = content

    def write(self, file) -> None:
        """Write config including raw sections."""
        super().write(file)

        existing_sections = self._sections
        for section, lines in self._raw_sections.items():
            if section not in existing_sections:
                file.write(f"\n[{section}]\n")
                for line in lines:
                    file.write(f"{line}\n")
