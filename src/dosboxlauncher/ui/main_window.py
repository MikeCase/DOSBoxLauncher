"""Main window UI for DOSBox Launcher."""

import subprocess

import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk

from ..config import load_app_config
from ..exceptions import ConfigError
from ..models import Game


class MainWindow(Gtk.ApplicationWindow):
    """Main window for the DOSBox Launcher."""

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(application=app, title="DOSBox Launcher")

        try:
            self.config = load_app_config()
        except ConfigError as e:
            self._show_error_dialog(f"Failed to load configuration: {e}")
            self.config = None

        self.game_library = self.config.games if self.config else None
        self._is_launching = False

        builder = Gtk.Builder()
        try:
            builder.add_from_file("UI/dosboxfe-v2.ui")
        except Exception as e:
            self._show_error_dialog(f"Error loading UI: {e}")
            return

        hwind = builder.get_object("hWind")
        if not hwind:
            self._show_error_dialog("Error: Main window not found in UI file.")
            return

        self.set_default_size(400, 550)

        child = hwind.get_child()
        if child:
            hwind.remove(child)
            self.add(child)

        self.game_list: Gtk.ListBox = builder.get_object("game_list")
        self.add_game_btn: Gtk.Button = builder.get_object("addGameBtn")
        self.edit_config_btn: Gtk.Button = builder.get_object("edit_config_btn")
        self.launch_game_btn: Gtk.Button = builder.get_object("launch_game_btn")
        self.search_entry: Gtk.SearchEntry | None = builder.get_object("search_entry")

        self.add_game_btn.connect("clicked", self._on_add_game_clicked)
        self.edit_config_btn.connect("clicked", self._on_edit_config_clicked)
        self.launch_game_btn.connect("clicked", self._on_launch_game_clicked)
        self.game_list.connect("button-press-event", self._on_game_list_button_press)
        if self.search_entry:
            self.search_entry.connect("search_changed", self._on_search_changed)

        self._refresh_game_list()

    def _show_error_dialog(self, message: str, title: str = "Error") -> None:
        """Show an error dialog to the user."""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def _show_info_dialog(self, message: str, title: str = "Info") -> None:
        """Show an info dialog to the user."""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def _reload_config(self) -> None:
        """Reload configuration from disk."""
        self.config = load_app_config()
        self.game_library = self.config.games

    def _refresh_game_list(self, games: list[Game] | None = None) -> None:
        """Refresh the game list display."""
        for child in self.game_list.get_children():
            self.game_list.remove(child)

        games = games or self.game_library.all()
        for game in games:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=game.name)
            label.set_xalign(0)
            row.add(label)
            row.show_all()
            row.game = game
            self.game_list.add(row)

    def _on_game_list_button_press(self, _widget: Gtk.ListBox, event: Gdk.EventButton) -> bool:
        """Launch a game only on mouse double-click."""
        if event.button != Gdk.BUTTON_PRIMARY:
            return False

        if event.type != Gdk.EventType.DOUBLE_BUTTON_PRESS:
            return False

        row = self.game_list.get_row_at_y(int(event.y))
        if not hasattr(row, "game"):
            return False

        self._launch_game(row.game)
        return True

    def _on_search_changed(self, entry: Gtk.SearchEntry) -> None:
        """Filter games based on search query."""
        query = entry.get_text()
        if not self.search_entry:
            return
        if query:
            filtered = self.game_library.search(query)
            self._refresh_game_list(filtered)
        else:
            self._refresh_game_list()

    def _on_add_game_clicked(self, btn: Gtk.Button) -> None:
        """Open the add game dialog."""
        from .add_game_dialog import AddGameDialog

        def on_game_added():
            self._reload_config()
            self._refresh_game_list()

        AddGameDialog(self, on_game_added=on_game_added)

    def _on_edit_config_clicked(self, btn: Gtk.Button) -> None:
        """Open the config editor for selected game."""
        selected = self.game_list.get_selected_row()
        if selected and hasattr(selected, "game"):
            from ..config_editor.editor import ConfigEditor

            ConfigEditor(self, selected.game)
        else:
            self._show_error_dialog("Please select a game first.")

    def _on_launch_game_clicked(self, btn: Gtk.Button) -> None:
        """Launch the selected game with DOSBox."""
        if self._is_launching:
            return

        selected = self.game_list.get_selected_row()
        if not selected or not hasattr(selected, "game"):
            self._show_error_dialog("Please select a game first.")
            return

        self._launch_game(selected.game)

    def _launch_game(self, game: Game) -> None:
        """Launch a specific game with DOSBox."""
        if self._is_launching:
            return

        is_valid, errors = game.validate(check_config_file=False)

        if not is_valid:
            self._show_error_dialog(f"Cannot launch {game.name}:\n" + "\n".join(errors))
            return

        config_file = game.get_config_file_path()

        self._is_launching = True
        self.launch_game_btn.set_sensitive(False)

        try:
            subprocess.Popen(["dosbox", "-conf", config_file])
        except FileNotFoundError:
            self._show_error_dialog(
                "DOSBox is not installed or not found in PATH. "
                "Please install DOSBox to launch games."
            )
        finally:
            self._is_launching = False
            self.launch_game_btn.set_sensitive(True)
