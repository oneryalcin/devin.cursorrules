from typer.testing import CliRunner
from devin_cursorrules.cli.main import app
from pathlib import Path
import pytest

runner = CliRunner()

def test_version():
    """Test the version command returns the correct version"""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "devin-cli" in result.stdout
    assert "version:" in result.stdout

def test_version_no_args():
    """Test CLI with no arguments shows help"""
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Usage:" in result.stdout

def test_init_default_path(tmp_path):
    """Test init command with default path"""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert "Successfully initialized" in result.stdout
        assert Path(td, ".cursorrules").exists()

def test_init_existing_file(tmp_path):
    """Test init command with existing file"""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        Path(td, ".cursorrules").touch()
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 1
        assert "already exists" in result.stdout

def test_init_force(tmp_path):
    """Test init command with force flag"""
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        Path(td, ".cursorrules").touch()
        result = runner.invoke(app, ["init", "--force"])
        assert result.exit_code == 0
        assert "Successfully initialized" in result.stdout