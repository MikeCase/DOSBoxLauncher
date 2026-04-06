"""Add game dialog."""

import os
from collections.abc import Callable

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ..config import get_games_dir
from ..config import load_app_config as load_config
from ..config import save_app_config as save_config
from ..models import Game


class AddGameDialog(Gtk.Dialog):
    """Dialog for adding a new game to the library."""

    def __init__(self, parent: Gtk.Window, on_game_added: Callable[[], None] | None = None) -> None:
        super().__init__(title="Add Game", transient_for=parent, flags=0)

        self.on_game_added = on_game_added

        builder = Gtk.Builder()
        builder.add_from_file("UI/addgamedlg.ui")

        self.dialog = builder.get_object("add_game_dialog")
        self.game_name_entry: Gtk.Entry = builder.get_object("game_name_entry")
        self.exe_path_entry: Gtk.Entry = builder.get_object("exe_path_entry")
        self.config_path_entry: Gtk.Entry = builder.get_object("config_file_entry")

        save_button = builder.get_object("save_button")
        cancel_button = builder.get_object("cancel_button")
        choose_exe_btn = builder.get_object("choose_exe_btn")
        choose_path_btn = builder.get_object("choose_path_btn")

        save_button.connect("clicked", self._on_save_clicked)
        cancel_button.connect("clicked", self._on_cancel_clicked)
        choose_exe_btn.connect("clicked", self._on_choose_exe_clicked)
        choose_path_btn.connect("clicked", self._on_choose_path_clicked)

        self.dialog.show()

    def _show_error(self, message: str) -> None:
        """Show error dialog."""
        dialog = Gtk.MessageDialog(
            transient_for=self.dialog,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error",
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def _on_save_clicked(self, btn: Gtk.Button) -> None:
        """Save the new game."""
        name = self.game_name_entry.get_text().strip()
        exe_path = self.exe_path_entry.get_text().strip()
        config_path = self.config_path_entry.get_text().strip()

        if not name:
            self._show_error("Game name is required.")
            return

        if not exe_path or not os.path.exists(exe_path):
            self._show_error("Game executable not found. Please select a valid executable.")
            return

        if not config_path or not os.path.isdir(config_path):
            self._show_error("Config directory not found. Please select a valid directory.")
            return

        games_dir = get_games_dir()
        game = Game(
            name=name,
            exe_path=exe_path,
            config_path=config_path,
        )

        self._create_game_config(game, games_dir)

        config = load_config()
        config.games.add(game)
        save_config(config)

        self.dialog.destroy()

        if self.on_game_added:
            self.on_game_added()

    def _on_cancel_clicked(self, btn: Gtk.Button) -> None:
        """Close the dialog without saving."""
        self.dialog.destroy()

    def _on_choose_exe_clicked(self, btn: Gtk.Button) -> None:
        """Open file chooser for game executable."""
        chooser = Gtk.FileChooserDialog(
            title="Select Game Executable",
            parent=self.dialog,
            action=Gtk.FileChooserAction.OPEN,
        )
        chooser.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        chooser.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT)
        chooser.connect("response", self._on_exe_chosen)
        chooser.show()

    def _on_exe_chosen(self, dialog: Gtk.FileChooserDialog, response_id: int) -> None:
        """Handle executable selection."""
        if response_id == Gtk.ResponseType.ACCEPT:
            path = dialog.get_filename()
            if path:
                self.exe_path_entry.set_text(path)
        dialog.destroy()

    def _on_choose_path_clicked(self, btn: Gtk.Button) -> None:
        """Open folder chooser for config directory."""
        chooser = Gtk.FileChooserDialog(
            title="Select Config Directory",
            parent=self.dialog,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        chooser.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        chooser.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT)
        chooser.connect("response", self._on_path_chosen)
        chooser.show()

    def _on_path_chosen(self, dialog: Gtk.FileChooserDialog, response_id: int) -> None:
        """Handle directory selection."""
        if response_id == Gtk.ResponseType.ACCEPT:
            path = dialog.get_filename()
            if path:
                self.config_path_entry.set_text(path)
        dialog.destroy()

    def _create_game_config(self, game: Game, games_dir) -> None:
        """Create default config file for the game."""
        default_config_path = games_dir / "base-config.conf"
        game_config_path = game.get_config_file_path()

        if not default_config_path.exists():
            default_config_path = "base-config.conf"

        if os.path.exists(default_config_path):
            with open(default_config_path) as reader:
                with open(game_config_path, "w") as writer:
                    writer.write(reader.read())
