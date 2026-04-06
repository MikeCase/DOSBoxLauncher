"""Tests for main window launch behavior."""

from unittest.mock import MagicMock

import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk

from dosboxlauncher.ui.main_window import MainWindow

DOUBLE_CLICK = Gdk.EventType.DOUBLE_BUTTON_PRESS


class TestMainWindowLaunchBehavior:
    def test_launch_button_uses_shared_launch_helper(self, sample_game):
        window = MainWindow.__new__(MainWindow)
        row = MagicMock()
        row.game = sample_game

        window._is_launching = False
        window.game_list = MagicMock()
        window.game_list.get_selected_row.return_value = row
        window._show_error_dialog = MagicMock()
        window._launch_game = MagicMock()

        window._on_launch_game_clicked(MagicMock())

        window._launch_game.assert_called_once_with(sample_game)

    def test_list_double_left_click_uses_shared_launch_helper(self, sample_game):
        window = MainWindow.__new__(MainWindow)
        row = MagicMock()
        row.game = sample_game
        event = MagicMock()
        event.button = 1
        event.type = DOUBLE_CLICK
        event.y = 10

        window.game_list = MagicMock()
        window.game_list.get_row_at_y.return_value = row
        window._launch_game = MagicMock()

        handled = window._on_game_list_button_press(MagicMock(), event)

        assert handled is True
        window._launch_game.assert_called_once_with(sample_game)

    def test_list_single_click_does_not_launch(self, sample_game):
        window = MainWindow.__new__(MainWindow)
        event = MagicMock()
        event.button = 1
        event.type = Gdk.EventType.BUTTON_PRESS

        window.game_list = MagicMock()
        window._launch_game = MagicMock()

        handled = window._on_game_list_button_press(MagicMock(), event)

        assert handled is False
        window._launch_game.assert_not_called()

    def test_list_double_right_click_does_not_launch(self, sample_game):
        window = MainWindow.__new__(MainWindow)
        event = MagicMock()
        event.button = 3
        event.type = DOUBLE_CLICK

        window.game_list = MagicMock()
        window._launch_game = MagicMock()

        handled = window._on_game_list_button_press(MagicMock(), event)

        assert handled is False
        window._launch_game.assert_not_called()

    def test_list_double_click_empty_space_does_not_launch(self):
        window = MainWindow.__new__(MainWindow)
        event = MagicMock()
        event.button = 1
        event.type = DOUBLE_CLICK
        event.y = 999

        window.game_list = MagicMock()
        window.game_list.get_row_at_y.return_value = None
        window._launch_game = MagicMock()

        handled = window._on_game_list_button_press(MagicMock(), event)

        assert handled is False
        window._launch_game.assert_not_called()
