"""Tests for DOSBox configuration parser."""

import pytest

from dosboxlauncher.config_editor.parser import DOSBoxConfigParser


class TestDOSBoxConfigParser:
    def test_parse_basic_config(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "test.conf"
        config_path.write_text("[sdl]\nfullscreen=false\noutput=surface\n")

        result = config.read(str(config_path))
        assert len(result) == 1
        assert config["sdl"]["fullscreen"] == "false"
        assert config["sdl"]["output"] == "surface"

    def test_parse_config_with_sections(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "test.conf"
        config_path.write_text("[sdl]\nfullscreen=false\n[dosbox]\nmachine=svga_s3\nmemsize=16\n")

        config.read(str(config_path))
        assert config["sdl"]["fullscreen"] == "false"
        assert config["dosbox"]["machine"] == "svga_s3"
        assert config["dosbox"]["memsize"] == "16"

    def test_get_raw_section_autoexec(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "test.conf"
        config_path.write_text("[autoexec]\nMOUNT C C:\\GAMES\nC:\n")

        config.read(str(config_path))
        raw = config.get_raw_section("autoexec")
        assert "MOUNT C C:\\GAMES" in raw

    def test_get_raw_section_missing(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "test.conf"
        config_path.write_text("[sdl]\nfullscreen=false\n")

        config.read(str(config_path))
        raw = config.get_raw_section("autoexec")
        assert raw == ""

    def test_set_raw_section(self):
        config = DOSBoxConfigParser()
        config.set_raw_section("autoexec", "MOUNT C C:\\GAMES\nC:")
        raw = config.get_raw_section("autoexec")
        assert "MOUNT C C:\\GAMES" in raw

    def test_set_raw_section_from_string(self):
        config = DOSBoxConfigParser()
        config.set_raw_section("autoexec", "MOUNT C C:\\GAMES\nC:")
        lines = config._raw_sections["autoexec"]
        assert len(lines) == 2

    def test_write_basic_config(self, tmp_path):
        config = DOSBoxConfigParser()
        config.read_string("[sdl]\nfullscreen=false\n")

        output_path = tmp_path / "output.conf"
        with open(output_path, "w") as f:
            config.write(f)

        content = output_path.read_text()
        assert "fullscreen" in content

    def test_write_with_raw_sections(self, tmp_path):
        config = DOSBoxConfigParser()
        config.read_string("[sdl]\nfullscreen=false\n")
        config.set_raw_section("autoexec", "MOUNT C C:\\GAMES\nC:")

        output_path = tmp_path / "output.conf"
        with open(output_path, "w") as f:
            config.write(f)

        content = output_path.read_text()
        assert "fullscreen" in content
        assert "MOUNT C C:\\GAMES" in content
        assert "[autoexec]" in content

    def test_read_nonexistent_file(self):
        config = DOSBoxConfigParser()
        result = config.read("/nonexistent/file.conf")
        assert result == []

    def test_roundtrip_with_raw_sections(self, tmp_path):
        original = DOSBoxConfigParser()
        original.read_string("[sdl]\noutput=surface\n")
        original.set_raw_section("autoexec", "MOUNT C C:\\DOSGAMES\nC:")

        output_path = tmp_path / "roundtrip.conf"
        with open(output_path, "w") as f:
            original.write(f)

        restored = DOSBoxConfigParser()
        restored.read(str(output_path))

        assert restored["sdl"]["output"] == "surface"
        assert "MOUNT C C:\\DOSGAMES" in restored.get_raw_section("autoexec")

    def test_read_file_without_autoexec(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "no_autoexec.conf"
        config_path.write_text("[sdl]\nfullscreen=false\n[cpu]\ncore=auto\n")

        config.read(str(config_path))
        raw = config.get_raw_section("autoexec")
        assert raw == ""

    def test_parser_handles_empty_lines(self, tmp_path):
        config = DOSBoxConfigParser()
        config_path = tmp_path / "test.conf"
        config_path.write_text("[sdl]\nfullscreen=false\n\n[dosbox]\nmemsize=16\n")

        config.read(str(config_path))
        assert config["sdl"]["fullscreen"] == "false"
        assert config["dosbox"]["memsize"] == "16"
