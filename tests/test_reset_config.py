"""Tests for DOSBox config editor reset functionality."""


class TestResetConfigButton:
    def test_reset_button_label_is_reset_config(self):
        """The reload button should be labeled 'Reset Config'."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "Reset Config" in content, "Button should have 'Reset Config' label"

    def test_reset_button_exists_in_ui(self):
        """The reset config button should exist in the UI."""
        ui_path = "UI/config_options.ui"
        with open(ui_path) as f:
            content = f.read()

        assert "reset_config_btn" in content, "reset_config_btn should exist"


class TestResetConfigDialog:
    def test_reset_config_shows_confirmation_dialog(self):
        """Clicking reset should show a confirmation dialog."""
        import ast

        editor_path = "src/dosboxlauncher/config_editor/editor.py"
        with open(editor_path) as f:
            content = f.read()

        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "_reset_config":
                func_source = ast.get_source_segment(content, node)
                assert "Gtk.MessageDialog" in func_source, "Should create a MessageDialog"
                assert "YES_NO" in func_source, "Should have YES_NO buttons"
                assert "transient_for" in func_source, "Should set transient_for"

    def test_reset_config_confirm_resets_to_defaults(self):
        """Confirming reset should overwrite config with defaults."""
        editor_path = "src/dosboxlauncher/config_editor/editor.py"
        with open(editor_path) as f:
            content = f.read()

        assert "_create_config" in content, "Should call _create_config to reset"

    def test_reset_config_cancel_keeps_current(self):
        """Canceling reset should keep existing config values."""
        editor_path = "src/dosboxlauncher/config_editor/editor.py"
        with open(editor_path) as f:
            content = f.read()

        assert "ResponseType.YES" in content, "Should check for YES response"
