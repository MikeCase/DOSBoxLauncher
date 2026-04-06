"""Data models for DOSBox Launcher."""

import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .exceptions import GameNotFoundError


@dataclass
class Game:
    """Represents a DOS game in the library."""

    name: str
    exe_path: str
    config_path: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    notes: str = ""

    def __post_init__(self) -> None:
        # Handle deserialization from dict/JSON
        if isinstance(self.id, str) and self.id:
            self.id = uuid.UUID(self.id)
        if isinstance(self.created_at, str) and self.created_at:
            self.created_at = datetime.fromisoformat(self.created_at)

    def validate(self, check_config_file: bool = True) -> tuple[bool, list[str]]:
        """Validate that game paths exist and are accessible.

        Args:
            check_config_file: If True, validate that config file exists.

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        if not self.name:
            errors.append("Game name cannot be empty")

        if not self.exe_path or not os.path.exists(self.exe_path):
            errors.append(f"Game executable not found: {self.exe_path}")

        if not self.config_path or not os.path.isdir(self.config_path):
            errors.append(f"Config directory not found: {self.config_path}")

        if check_config_file:
            config_file = self.get_config_file_path()
            if not os.path.exists(config_file):
                errors.append(f"Config file not found: {config_file}")

        return len(errors) == 0, errors

    def get_config_file_path(self) -> str:
        """Get the full path to the game's DOSBox config file."""
        return os.path.join(self.config_path, f"{self.id}.conf")

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": str(self.id),
            "name": self.name,
            "exe_path": self.exe_path,
            "config_path": self.config_path,
            "created_at": self.created_at.isoformat(),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Game":
        """Create Game from dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            exe_path=data.get("exe_path", ""),
            config_path=data.get("config_path", ""),
            created_at=data.get("created_at", ""),
            notes=data.get("notes", ""),
        )


class GameLibrary:
    """Manages the collection of games."""

    def __init__(self, games: list[Game] | None = None):
        self._games: list[Game] = games or []

    def add(self, game: Game) -> None:
        """Add a game to the library."""
        self._games.append(game)

    def remove(self, game_id: uuid.UUID) -> Game:
        """Remove a game by ID."""
        for i, game in enumerate(self._games):
            if game.id == game_id:
                return self._games.pop(i)
        raise GameNotFoundError(f"Game with ID {game_id} not found")

    def get(self, game_id: uuid.UUID) -> Game | None:
        """Get a game by ID."""
        for game in self._games:
            if game.id == game_id:
                return game
        return None

    def get_by_name(self, name: str) -> Game | None:
        """Get a game by name (case-insensitive)."""
        name_lower = name.lower()
        for game in self._games:
            if game.name.lower() == name_lower:
                return game
        return None

    def search(self, query: str) -> list[Game]:
        """Search games by name (case-insensitive)."""
        query_lower = query.lower()
        return [g for g in self._games if query_lower in g.name.lower()]

    def all(self) -> list[Game]:
        """Get all games."""
        return self._games.copy()

    def __len__(self) -> int:
        return len(self._games)

    def __iter__(self):
        return iter(self._games)

    def to_dict(self) -> dict:
        """Serialize library to dictionary."""
        return {"games": [g.to_dict() for g in self._games]}

    @classmethod
    def from_dict(cls, data: dict) -> "GameLibrary":
        """Create library from dictionary."""
        games = [Game.from_dict(g) for g in data.get("games", [])]
        return cls(games)
