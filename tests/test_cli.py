import pytest

def test_version(runner, cli_app):
    """Test the version command returns the correct version"""
    result = runner.invoke(cli_app, ["--version"])
    assert result.exit_code == 0
    assert "devin-cli" in result.stdout
    assert "version:" in result.stdout

def test_version_no_args(runner, cli_app):
    """Test CLI with no arguments shows help"""
    result = runner.invoke(cli_app)
    assert result.exit_code == 0
    assert "Usage:" in result.stdout

def test_init_default_path(isolated_cli_runner, cli_app):
    """Test init command with default path"""
    runner, td = isolated_cli_runner
    result = runner.invoke(cli_app, ["init"])
    assert result.exit_code == 0
    assert "Successfully initialized" in result.stdout
    assert (td / ".cursorrules").exists()

def test_init_existing_file(isolated_cli_runner, cli_app):
    """Test init command with existing file"""
    runner, td = isolated_cli_runner
    (td / ".cursorrules").touch()
    result = runner.invoke(cli_app, ["init"])
    assert result.exit_code == 1
    assert "already exists" in result.stdout

def test_init_force(isolated_cli_runner, cli_app):
    """Test init command with force flag"""
    runner, td = isolated_cli_runner
    (td / ".cursorrules").touch()
    result = runner.invoke(cli_app, ["init", "--force"])
    assert result.exit_code == 0
    assert "Successfully initialized" in result.stdout