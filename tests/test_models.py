"""Tests for DOSBox Launcher models."""

import uuid

import pytest

from dosboxlauncher.models import Game, GameLibrary


class TestGame:
    def test_create_game(self, tmp_path):
        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")
        config_path = tmp_path / "config"
        config_path.mkdir()
        config_file = config_path / f"{uuid.uuid4()}.conf"
        config_file.write_text("[autoexec]\n")

        game = Game(
            name="Test Game",
            exe_path=str(exe_path),
            config_path=str(config_path),
        )

        assert game.name == "Test Game"
        assert game.exe_path == str(exe_path)
        assert game.config_path == str(config_path)
        assert game.id is not None

    def test_validate_valid_game(self, tmp_path):
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

        config_file = config_path / f"{game.id}.conf"
        config_file.write_text("[autoexec]\n")

        is_valid, errors = game.validate()
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_missing_exe(self, tmp_path):
        game = Game(
            name="Test Game",
            exe_path="/nonexistent/game.exe",
            config_path=str(tmp_path),
        )

        is_valid, errors = game.validate()
        assert is_valid is False
        assert any("executable" in e.lower() for e in errors)

    def test_validate_missing_config(self, tmp_path):
        config_path = tmp_path / "config"
        game = Game(
            name="Test Game",
            exe_path=str(tmp_path / "game.exe"),
            config_path=str(config_path),
        )

        is_valid, errors = game.validate()
        assert is_valid is False
        assert any("config" in e.lower() for e in errors)

    def test_to_dict(self, tmp_path):
        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")
        config_path = tmp_path / "config"
        config_path.mkdir()
        config_file = config_path / f"{uuid.uuid4()}.conf"
        config_file.write_text("[autoexec]\n")

        game = Game(
            name="Test Game",
            exe_path=str(exe_path),
            config_path=str(config_path),
        )

        data = game.to_dict()
        assert data["name"] == "Test Game"
        assert data["exe_path"] == str(exe_path)
        assert "id" in data

    def test_from_dict(self, tmp_path):
        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")
        config_path = tmp_path / "config"
        config_path.mkdir()

        data = {
            "name": "Test Game",
            "exe_path": str(exe_path),
            "config_path": str(config_path),
            "id": str(uuid.uuid4()),
        }

        game = Game.from_dict(data)
        assert game.name == "Test Game"


class TestGameLibrary:
    def test_create_empty_library(self):
        library = GameLibrary()
        assert len(library) == 0

    def test_add_game(self, tmp_path):
        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")
        config_path = tmp_path / "config"
        config_path.mkdir()
        config_file = config_path / f"{uuid.uuid4()}.conf"
        config_file.write_text("[autoexec]\n")

        game = Game(
            name="Test Game",
            exe_path=str(exe_path),
            config_path=str(config_path),
        )

        library = GameLibrary()
        library.add(game)
        assert len(library) == 1

    def test_remove_game(self, tmp_path):
        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")
        config_path = tmp_path / "config"
        config_path.mkdir()
        config_file = config_path / f"{uuid.uuid4()}.conf"
        config_file.write_text("[autoexec]\n")

        game = Game(
            name="Test Game",
            exe_path=str(exe_path),
            config_path=str(config_path),
        )

        library = GameLibrary()
        library.add(game)
        removed = library.remove(game.id)
        assert removed.id == game.id
        assert len(library) == 0

    def test_get_game(self, tmp_path):
        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")
        config_path = tmp_path / "config"
        config_path.mkdir()
        config_file = config_path / f"{uuid.uuid4()}.conf"
        config_file.write_text("[autoexec]\n")

        game = Game(
            name="Test Game",
            exe_path=str(exe_path),
            config_path=str(config_path),
        )

        library = GameLibrary()
        library.add(game)

        found = library.get(game.id)
        assert found is not None
        assert found.name == "Test Game"

    def test_search_games(self, tmp_path):
        config_path = tmp_path / "config"
        config_path.mkdir()

        library = GameLibrary()

        for name in ["Doom", "Duke Nukem", "Wolfenstein"]:
            game_dir = tmp_path / name.replace(" ", "_").lower()
            game_dir.mkdir()
            exe_path = game_dir / "game.exe"
            exe_path.write_text("")

            game = Game(
                name=name,
                exe_path=str(exe_path),
                config_path=str(config_path),
            )
            config_file = config_path / f"{game.id}.conf"
            config_file.write_text("[autoexec]\n")
            library.add(game)

        results = library.search("doom")
        assert len(results) == 1
        assert results[0].name == "Doom"

    def test_to_dict(self, tmp_path):
        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")
        config_path = tmp_path / "config"
        config_path.mkdir()
        config_file = config_path / f"{uuid.uuid4()}.conf"
        config_file.write_text("[autoexec]\n")

        game = Game(
            name="Test Game",
            exe_path=str(exe_path),
            config_path=str(config_path),
        )

        library = GameLibrary([game])
        data = library.to_dict()

        assert "games" in data
        assert len(data["games"]) == 1


class TestGameEdgeCases:
    def test_validate_empty_name(self, tmp_path):
        game = Game(
            name="",
            exe_path=str(tmp_path / "game.exe"),
            config_path=str(tmp_path),
        )

        is_valid, errors = game.validate(check_config_file=False)
        assert is_valid is False
        assert any("name" in e.lower() for e in errors)

    def test_validate_missing_config_file(self, tmp_path):
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

        is_valid, errors = game.validate(check_config_file=True)
        assert is_valid is False
        assert any("config file" in e.lower() for e in errors)

    def test_get_config_file_path(self, tmp_path):
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

        config_file_path = game.get_config_file_path()
        assert str(game.id) in config_file_path
        assert config_file_path.endswith(".conf")

    def test_get_by_name_exact(self, tmp_path):
        config_path = tmp_path / "config"
        config_path.mkdir()

        game = Game(
            name="Doom",
            exe_path=str(tmp_path / "game.exe"),
            config_path=str(config_path),
        )

        library = GameLibrary([game])
        found = library.get_by_name("Doom")
        assert found is not None
        assert found.name == "Doom"

    def test_get_by_name_case_insensitive(self, tmp_path):
        config_path = tmp_path / "config"
        config_path.mkdir()

        game = Game(
            name="Doom",
            exe_path=str(tmp_path / "game.exe"),
            config_path=str(config_path),
        )

        library = GameLibrary([game])
        found = library.get_by_name("doom")
        assert found is not None
        assert found.name == "Doom"

        found_upper = library.get_by_name("DOOM")
        assert found_upper is not None

    def test_get_by_name_not_found(self, tmp_path):
        library = GameLibrary()
        found = library.get_by_name("Nonexistent")
        assert found is None

    def test_library_remove_nonexistent(self):
        library = GameLibrary()
        from dosboxlauncher.exceptions import GameNotFoundError

        with pytest.raises(GameNotFoundError, match="not found"):
            library.remove(uuid.uuid4())

    def test_library_search_case_insensitive(self, tmp_path):
        config_path = tmp_path / "config"
        config_path.mkdir()

        library = GameLibrary()

        for name in ["DOOM", "doom", "Doom"]:
            game_dir = tmp_path / f"game_{name.lower()}"
            game_dir.mkdir(exist_ok=True)
            exe_path = game_dir / "game.exe"
            exe_path.write_text("")

            game = Game(
                name=name,
                exe_path=str(exe_path),
                config_path=str(config_path),
            )
            library.add(game)

        results = library.search("doom")
        assert len(results) == 3

    def test_game_serialization_roundtrip(self, tmp_path):
        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")
        config_path = tmp_path / "config"
        config_path.mkdir()

        original = Game(
            name="Test Game",
            exe_path=str(exe_path),
            config_path=str(config_path),
            notes="Test notes",
        )

        data = original.to_dict()
        restored = Game.from_dict(data)

        assert restored.name == original.name
        assert restored.exe_path == original.exe_path
        assert restored.config_path == original.config_path
        assert restored.notes == original.notes
        assert str(restored.id) == str(original.id)

    def test_game_notes_field(self, tmp_path):
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
            notes="This is a test game",
        )

        data = game.to_dict()
        assert data["notes"] == "This is a test game"

        restored = Game.from_dict(data)
        assert restored.notes == "This is a test game"

    def test_game_created_at(self, tmp_path):
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

        from datetime import datetime

        assert isinstance(game.created_at, datetime)

    def test_library_iteration(self, tmp_path):
        config_path = tmp_path / "config"
        config_path.mkdir()

        library = GameLibrary()

        for name in ["Game1", "Game2", "Game3"]:
            game_dir = tmp_path / name
            game_dir.mkdir()
            exe_path = game_dir / "game.exe"
            exe_path.write_text("")

            game = Game(
                name=name,
                exe_path=str(exe_path),
                config_path=str(config_path),
            )
            library.add(game)

        names = [g.name for g in library]
        assert "Game1" in names
        assert "Game2" in names
        assert "Game3" in names

    def test_library_len(self, tmp_path):
        config_path = tmp_path / "config"
        config_path.mkdir()

        library = GameLibrary()
        assert len(library) == 0

        for i in range(5):
            game_dir = tmp_path / f"game{i}"
            game_dir.mkdir()
            exe_path = game_dir / "game.exe"
            exe_path.write_text("")

            game = Game(
                name=f"Game{i}",
                exe_path=str(exe_path),
                config_path=str(config_path),
            )
            library.add(game)

        assert len(library) == 5

    def test_library_from_dict(self, tmp_path):
        config_path = tmp_path / "config"
        config_path.mkdir()

        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")

        game = Game(
            name="Test Game",
            exe_path=str(exe_path),
            config_path=str(config_path),
        )

        library = GameLibrary([game])
        data = library.to_dict()

        restored = GameLibrary.from_dict(data)
        assert len(restored) == 1

    def test_library_all(self, tmp_path):
        config_path = tmp_path / "config"
        config_path.mkdir()

        library = GameLibrary()

        for name in ["A", "B", "C"]:
            game_dir = tmp_path / name
            game_dir.mkdir()
            exe_path = game_dir / "game.exe"
            exe_path.write_text("")

            game = Game(
                name=name,
                exe_path=str(exe_path),
                config_path=str(config_path),
            )
            library.add(game)

        all_games = library.all()
        assert len(all_games) == 3
        assert all(isinstance(g, Game) for g in all_games)

    def test_library_all_returns_copy(self, tmp_path):
        config_path = tmp_path / "config"
        config_path.mkdir()

        game_dir = tmp_path / "game"
        game_dir.mkdir()
        exe_path = game_dir / "game.exe"
        exe_path.write_text("")

        game = Game(
            name="Test Game",
            exe_path=str(exe_path),
            config_path=str(config_path),
        )
        library = GameLibrary([game])

        all_games = library.all()
        all_games.clear()

        assert len(library) == 1

    def test_game_validate_without_config_file_check(self, tmp_path):
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

        is_valid, errors = game.validate(check_config_file=False)
        assert is_valid is True
        assert len(errors) == 0
