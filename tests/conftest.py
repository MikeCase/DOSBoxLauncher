"""Tests for DOSBox Launcher."""

import pytest

from dosboxlauncher.exceptions import (
    ConfigError,
    GameNotFoundError,
    LaunchError,
    ValidationError,
)
from dosboxlauncher.models import Game, GameLibrary


@pytest.fixture
def sample_game(tmp_path):
    """Create a sample game for testing."""
    game_dir = tmp_path / "game"
    game_dir.mkdir()
    exe_path = game_dir / "game.exe"
    exe_path.write_text("")
    config_path = tmp_path / "config"
    config_path.mkdir()
    config_file = config_path / "config.conf"
    config_file.write_text("[autoexec]\n")

    return Game(
        name="Test Game",
        exe_path=str(exe_path),
        config_path=str(config_path),
    )


@pytest.fixture
def game_library():
    """Create a game library for testing."""
    return GameLibrary()
