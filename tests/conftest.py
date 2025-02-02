import pytest
from typer.testing import CliRunner
from pathlib import Path
from devin_cursorrules.cli.main import app

@pytest.fixture
def runner():
    """Fixture that provides a CLI runner for testing commands."""
    return CliRunner()

@pytest.fixture
def cli_app():
    """Fixture that provides the CLI application instance."""
    return app

@pytest.fixture
def temp_dir(tmp_path):
    """Fixture that provides a temporary directory for file operations.
    
    This fixture wraps pytest's tmp_path fixture and provides additional setup/teardown
    if needed in the future.
    """
    return tmp_path

@pytest.fixture
def isolated_cli_runner(runner, temp_dir):
    """Fixture that provides a CLI runner with an isolated filesystem.
    
    This is useful for commands that need to perform file operations without affecting
    the actual filesystem.
    """
    with runner.isolated_filesystem(temp_dir=temp_dir) as td:
        yield runner, Path(td)