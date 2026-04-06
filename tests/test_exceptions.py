"""Tests for DOSBox Launcher exceptions."""

import pytest

from dosboxlauncher.exceptions import (
    ConfigError,
    DOSBoxLauncherError,
    GameNotFoundError,
    LaunchError,
    ValidationError,
)


class TestExceptionHierarchy:
    def test_base_exception_exists(self):
        assert issubclass(DOSBoxLauncherError, Exception)

    def test_game_not_found_inherits_from_base(self):
        assert issubclass(GameNotFoundError, DOSBoxLauncherError)

    def test_config_error_inherits_from_base(self):
        assert issubclass(ConfigError, DOSBoxLauncherError)

    def test_launch_error_inherits_from_base(self):
        assert issubclass(LaunchError, DOSBoxLauncherError)

    def test_validation_error_inherits_from_base(self):
        assert issubclass(ValidationError, DOSBoxLauncherError)


class TestGameNotFoundError:
    def test_can_be_raised_with_message(self):
        with pytest.raises(GameNotFoundError, match="Game not found"):
            raise GameNotFoundError("Game not found")

    def test_can_be_raised_without_message(self):
        with pytest.raises(GameNotFoundError):
            raise GameNotFoundError()

    def test_can_be_caught_as_base_exception(self):
        with pytest.raises(DOSBoxLauncherError):
            raise GameNotFoundError("Game not found")


class TestConfigError:
    def test_can_be_raised_with_message(self):
        with pytest.raises(ConfigError, match="Invalid config"):
            raise ConfigError("Invalid config")

    def test_can_be_caught_as_base_exception(self):
        with pytest.raises(DOSBoxLauncherError):
            raise ConfigError("Invalid config")


class TestLaunchError:
    def test_can_be_raised_with_message(self):
        with pytest.raises(LaunchError, match="DOSBox not found"):
            raise LaunchError("DOSBox not found")

    def test_can_be_caught_as_base_exception(self):
        with pytest.raises(DOSBoxLauncherError):
            raise LaunchError("DOSBox not found")


class TestValidationError:
    def test_can_be_raised_with_message(self):
        with pytest.raises(ValidationError, match="Invalid path"):
            raise ValidationError("Invalid path")

    def test_can_be_caught_as_base_exception(self):
        with pytest.raises(DOSBoxLauncherError):
            raise ValidationError("Invalid path")


class TestExceptionChaining:
    def test_can_chain_exceptions(self):
        with pytest.raises(ConfigError) as exc_info:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise ConfigError("Wrapped error") from e

        assert "Wrapped error" in str(exc_info.value)
        assert exc_info.value.__cause__ is not None


class TestExceptionEquality:
    def test_same_message_exceptions_equal(self):
        e1 = GameNotFoundError("Same message")
        e2 = GameNotFoundError("Same message")
        assert e1 != e2

    def test_different_message_exceptions_not_equal(self):
        e1 = GameNotFoundError("Message 1")
        e2 = GameNotFoundError("Message 2")
        assert e1 != e2
