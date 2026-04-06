"""Tests for DOSBox Launcher configuration module."""

import os

import pytest

from dosboxlauncher.config import (
    AppConfig,
    get_config_path,
    get_games_dir,
    load_app_config,
    save_app_config,
)
from dosboxlauncher.models import Game, GameLibrary


class TestAppConfig:
    def test_create_default_config(self):
        config = AppConfig()
        assert config.dosbox_path is None
        assert config.default_config_dir is None
        assert isinstance(config.games, GameLibrary)
        assert len(config.games) == 0

    def test_config_to_dict(self):
        config = AppConfig()
        data = config.to_dict()

        assert "dosbox_path" in data
        assert "default_config_dir" in data
        assert "games" in data

    def test_config_from_dict(self):
        data = {
            "dosbox_path": "/usr/bin/dosbox",
            "default_config_dir": "/home/user/dosbox-config",
            "games": {"games": []},
        }

        config = AppConfig.from_dict(data)
        assert config.dosbox_path == "/usr/bin/dosbox"
        assert config.default_config_dir == "/home/user/dosbox-config"
        assert isinstance(config.games, GameLibrary)

    def test_config_from_dict_with_games(self, tmp_path):
        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")
        config_path = tmp_path / "config"
        config_path.mkdir()

        game = Game(
            name="Test Game",
            exe_path=str(exe_path),
            config_path=str(config_path),
        )

        library = GameLibrary([game])
        config = AppConfig(games=library)
        data = config.to_dict()

        restored = AppConfig.from_dict(data)
        assert len(restored.games) == 1
        assert restored.games.all()[0].name == "Test Game"


class TestConfigPath:
    def test_get_config_path(self):
        path = get_config_path()
        assert isinstance(path, type(path))
        assert "DOSBoxLauncher" in str(path)
        assert path.name == "config.yaml"

    def test_get_games_dir(self):
        path = get_games_dir()
        assert "DOSBoxLauncher" in str(path)
        assert path.name == "games"


class TestLoadSaveConfig:
    def test_load_config_missing_file(self, tmp_path, monkeypatch):
        import dosboxlauncher.config as config_module

        monkeypatch.setattr(config_module, "get_config_path", lambda: tmp_path / "nonexistent.yaml")

        config = load_app_config()
        assert isinstance(config, AppConfig)

    def test_save_and_load_config(self, tmp_path, monkeypatch):
        import dosboxlauncher.config as config_module

        config_path = tmp_path / "config.yaml"
        monkeypatch.setattr(config_module, "get_config_path", lambda: config_path)

        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")
        config_path_dir = tmp_path / "config"
        config_path_dir.mkdir()

        game = Game(
            name="Test Game",
            exe_path=str(exe_path),
            config_path=str(config_path_dir),
        )

        config = AppConfig(dosbox_path="/usr/bin/dosbox", games=GameLibrary([game]))
        save_app_config(config)

        assert config_path.exists()

        loaded = load_app_config()
        assert loaded.dosbox_path == "/usr/bin/dosbox"
        assert len(loaded.games) == 1

    def test_save_config_creates_directory(self, tmp_path, monkeypatch):
        import dosboxlauncher.config as config_module

        nested_path = tmp_path / "nested" / "dir" / "config.yaml"
        monkeypatch.setattr(config_module, "get_config_path", lambda: nested_path)

        config = AppConfig()
        save_app_config(config)

        assert nested_path.exists()


class TestConfigErrors:
    def test_load_config_invalid_yaml(self, tmp_path, monkeypatch):
        import dosboxlauncher.config as config_module

        config_path = tmp_path / "invalid.yaml"
        config_path.write_text("invalid: yaml: content:")
        monkeypatch.setattr(config_module, "get_config_path", lambda: config_path)

        from dosboxlauncher.exceptions import ConfigError

        with pytest.raises(ConfigError, match="Invalid config file"):
            load_app_config()

    def test_load_config_permission_error(self, tmp_path, monkeypatch):
        import dosboxlauncher.config as config_module

        config_path = tmp_path / "config.yaml"
        config_path.write_text("")
        monkeypatch.setattr(config_module, "get_config_path", lambda: config_path)

        monkeypatch.setattr(
            os, "open", lambda *args, **kwargs: (_ for _ in ()).throw(PermissionError)
        )

        from dosboxlauncher.exceptions import ConfigError

        try:
            load_app_config()
        except ConfigError as e:
            assert "Failed to load config" in str(e)


class TestMigrateFromJson:
    def test_migrate_from_json_empty(self, tmp_path, monkeypatch):
        import dosboxlauncher.config as config_module

        config_path = tmp_path / "config.yaml"
        monkeypatch.setattr(config_module, "get_config_path", lambda: config_path)
        monkeypatch.setattr(config_module, "get_games_dir", lambda: tmp_path / "games")

        json_path = tmp_path / "games.json"
        json_path.write_text("[]")

        config = config_module.migrate_from_json(str(json_path))

        assert len(config.games) == 0

    def test_migrate_from_json_with_games(self, tmp_path, monkeypatch):
        import dosboxlauncher.config as config_module

        config_path = tmp_path / "config.yaml"
        monkeypatch.setattr(config_module, "get_config_path", lambda: config_path)
        monkeypatch.setattr(config_module, "get_games_dir", lambda: tmp_path / "games")

        json_path = tmp_path / "games.json"
        json_path.write_text(
            '[{"name": "Game1", "config_file": "/path/to/config1"}, {"name": "Game2", "config_file": "/path/to/config2"}]'
        )

        config = config_module.migrate_from_json(str(json_path))

        assert len(config.games) == 2

    def test_migrate_from_json_nonexistent(self, tmp_path, monkeypatch):
        import dosboxlauncher.config as config_module

        config_path = tmp_path / "config.yaml"
        monkeypatch.setattr(config_module, "get_config_path", lambda: config_path)

        config = config_module.migrate_from_json("/nonexistent/games.json")

        assert isinstance(config, AppConfig)

    def test_migrate_from_json_invalid_format(self, tmp_path, monkeypatch):
        import dosboxlauncher.config as config_module

        config_path = tmp_path / "config.yaml"
        monkeypatch.setattr(config_module, "get_config_path", lambda: config_path)

        json_path = tmp_path / "games.json"
        json_path.write_text("not valid json")

        config = config_module.migrate_from_json(str(json_path))

        assert isinstance(config, AppConfig)
