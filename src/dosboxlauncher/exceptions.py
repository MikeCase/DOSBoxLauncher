"""Custom exceptions for DOSBox Launcher."""


class DOSBoxLauncherError(Exception):
    """Base exception for DOSBox Launcher."""
    pass


class GameNotFoundError(DOSBoxLauncherError):
    """Raised when a game cannot be found."""
    pass


class ConfigError(DOSBoxLauncherError):
    """Raised when there's an issue with configuration."""
    pass


class LaunchError(DOSBoxLauncherError):
    """Raised when a game fails to launch."""
    pass


class ValidationError(DOSBoxLauncherError):
    """Raised when validation fails."""
    pass
