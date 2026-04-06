"""Application configuration management."""

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from platformdirs import PlatformDirs

from .exceptions import ConfigError
from .models import GameLibrary

APP_NAME = "DOSBoxLauncher"
APP_AUTHOR = "DOSBoxLauncher"


@dataclass
class AppConfig:
    """Application configuration."""

    dosbox_path: str | None = None
    default_config_dir: str | None = None
    games: GameLibrary = field(default_factory=GameLibrary)

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization."""
        return {
            "dosbox_path": self.dosbox_path,
            "default_config_dir": self.default_config_dir,
            "games": self.games.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AppConfig":
        """Create AppConfig from dictionary."""
        games_data = data.get("games", {})
        return cls(
            dosbox_path=data.get("dosbox_path"),
            default_config_dir=data.get("default_config_dir"),
            games=GameLibrary.from_dict(games_data),
        )


def get_app_dirs() -> PlatformDirs:
    """Get platform-specific application directories."""
    return PlatformDirs(APP_NAME, APP_AUTHOR)


def get_config_path() -> Path:
    """Get path to the config file."""
    dirs = get_app_dirs()
    config_dir = Path(dirs.user_config_dir)
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.yaml"


def get_games_dir() -> Path:
    """Get path to the games config directory."""
    dirs = get_app_dirs()
    games_dir = Path(dirs.user_data_dir) / "games"
    games_dir.mkdir(parents=True, exist_ok=True)
    return games_dir


def load_app_config() -> AppConfig:
    """Load application configuration from YAML file."""
    config_path = get_config_path()

    if not config_path.exists():
        return AppConfig()

    try:
        with open(config_path) as f:
            data = yaml.safe_load(f) or {}
        return AppConfig.from_dict(data)
    except yaml.YAMLError as e:
        raise ConfigError(f"Invalid config file: {e}") from e
    except Exception as e:
        raise ConfigError(f"Failed to load config: {e}") from e


def save_app_config(config: AppConfig) -> None:
    """Save application configuration to YAML file."""
    config_path = get_config_path()

    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w") as f:
        yaml.dump(config.to_dict(), f, default_flow_style=False, sort_keys=False)


def migrate_from_json(json_path: str = "games.json") -> AppConfig:
    """Migrate games from old JSON format to new YAML config."""
    import json

    config = load_app_config()

    if not os.path.exists(json_path):
        return config

    try:
        with open(json_path) as f:
            old_games = json.load(f)

        for old_game in old_games:
            from .models import Game

            # Old format didn't have exe path - leave blank for user to fill
            game = Game(
                name=old_game.get("name", "Unknown"),
                exe_path="",
                config_path=old_game.get("config_file", ""),
            )
            config.games.add(game)

        save_app_config(config)
    except Exception:
        pass  # Silent failure for migration - old file may not exist

    return config
