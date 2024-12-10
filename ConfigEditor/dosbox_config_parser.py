import configparser
from pprint import pprint

## Use the custom parser
# config = CustomConfigParser()
# config.read("config.ini")

## Get a normal setting
# print("Theme:", config["Settings"]["theme"])

## Get the raw AutoExec section
# autoexec_script = config.get_raw_section("AutoExec")
# print("\nAutoExec Section:")
# print(autoexec_script)

## Write the raw autoexec section
# autoexec_script = config.set_raw_section("AutoExec", new_content)
## save changes to file.
# with open("new_config.conf|ini|whatever", "w") as f:
#     config.write(f)

class DOSBoxConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_sections = {}

    def read(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()

        current_section = None
        for line in lines:
            line = line.rstrip("\n")
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
                if current_section not in self.raw_sections:
                    self.raw_sections[current_section] = []
            elif current_section and "=" not in line.strip():
                self.raw_sections[current_section].append(line)
            else:
                super().read_string(f"[{current_section}]\n{line}" if current_section else line)

    def get_raw_section(self, section):
        return "\n".join(self.raw_sections.get(section, []))
    
    def set_raw_section(self, section, content):
        """
        Sets or updates the raw content of a section.
        :param section: The name of the section.
        :param content: A string or list of lines to store as raw text.
        """
        if isinstance(content, str):
            content = content.splitlines()
        self.raw_sections[section] = content

    def write(self, file):
        """
        Write the configuration, including raw sections, to the provided file-like object.
        """
        # First, write standard sections
        super().write(file)

        # Then write raw sections
        # pprint(self.raw_sections)
        for section, lines in self.raw_sections.items():
            # print(f"{section} | {lines}")
            if section == 'autoexec':
                file.write(f"\n[{section}]\n")
                for line in lines:
                    file.write(f"{line}\n")

