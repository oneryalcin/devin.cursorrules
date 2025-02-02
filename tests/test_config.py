import pytest
import os
from pathlib import Path
from devin_cursorrules.config import DevinSettings

def test_settings_default_values():
    """Test default values of settings"""
    settings = DevinSettings()
    assert settings.api_key is None
    assert settings.project_path is None
    assert settings.default_model == "gpt-4"
    assert settings.max_tokens == 4096
    assert settings.temperature == 0.7

def test_settings_load_save(tmp_path):
    """Test loading and saving settings"""
    env_file = tmp_path / ".env"
    settings = DevinSettings(
        api_key="test-key",
        project_path=str(tmp_path),
        default_model="gpt-3.5-turbo"
    )
    
    # Change to temp directory to test save
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        settings.save()
        assert env_file.exists()
        
        # Load settings and verify
        new_settings = DevinSettings.load()
        assert new_settings.api_key.get_secret_value() == "test-key"
        assert str(new_settings.project_path) == str(tmp_path)
        assert new_settings.default_model == "gpt-3.5-turbo"
    finally:
        os.chdir(original_cwd)

def test_config_cli_commands(isolated_cli_runner, cli_app):
    """Test config CLI commands"""
    runner, td = isolated_cli_runner
    
    # Test setting a value
    result = runner.invoke(cli_app, ["config", "set", "api_key", "test-key"])
    assert result.exit_code == 0
    assert "Set api_key to test-key" in result.stdout
    
    # Test getting a specific value
    result = runner.invoke(cli_app, ["config", "get", "api_key"])
    assert result.exit_code == 0
    assert "api_key: test-key" in result.stdout
    
    # Test getting all values
    result = runner.invoke(cli_app, ["config", "get"])
    assert result.exit_code == 0
    assert "api_key: test-key" in result.stdout
    assert "project_path: not set" in result.stdout
    
    # Test setting invalid key
    result = runner.invoke(cli_app, ["config", "set", "invalid_key", "value"])
    assert result.exit_code == 1
    assert "Unknown configuration key" in result.stdout