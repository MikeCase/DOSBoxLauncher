"""Tests for DOSBox Launcher __main__ module."""

import pytest


class TestMainModule:
    def test_module_imports(self):
        """Test that the module can be imported."""
        import dosboxlauncher.__main__ as main_module

        assert main_module is not None

    def test_main_function_exists(self):
        """Test that main function exists."""
        import dosboxlauncher.__main__ as main_module

        assert hasattr(main_module, "main")
        assert callable(main_module.main)

    def test_dosbox_launcher_app_exists(self):
        """Test that DOSBoxLauncherApp class exists."""
        import dosboxlauncher.__main__ as main_module

        assert hasattr(main_module, "DOSBoxLauncherApp")

    def test_module_exports(self):
        """Test module exports."""
        import dosboxlauncher.__main__ as main_module

        exports = dir(main_module)
        assert "main" in exports
        assert "DOSBoxLauncherApp" in exports
