import pytest
import os
import keyring
from pathlib import Path
from pydantic import SecretStr
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
    assert "Set api_key to ********" in result.stdout
    
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

def test_api_key_validation():
    """Test API key validation"""
    # Test short API key
    with pytest.raises(ValueError, match="API key seems too short"):
        DevinSettings(api_key=SecretStr("short"))
    
    # Test valid API key
    settings = DevinSettings(api_key=SecretStr("a" * 20))
    assert settings.api_key.get_secret_value() == "a" * 20

def test_secure_storage():
    """Test secure storage using keyring"""
    test_key = "test-secure-key"
    
    # Set API key and save
    settings = DevinSettings(api_key=SecretStr(test_key))
    settings.save()
    
    # Verify key is in keyring
    stored_key = keyring.get_password("devin-cli", "api_key")
    assert stored_key == test_key
    
    # Load settings and verify key is retrieved
    new_settings = DevinSettings.load()
    assert new_settings.api_key.get_secret_value() == test_key

def test_environment_variables():
    """Test loading settings from environment variables"""
    os.environ["DEVIN_API_KEY"] = "env-test-key"
    os.environ["DEVIN_DEFAULT_MODEL"] = "gpt-3.5-turbo"
    
    try:
        settings = DevinSettings()
        assert settings.api_key.get_secret_value() == "env-test-key"
        assert settings.default_model == "gpt-3.5-turbo"
    finally:
        del os.environ["DEVIN_API_KEY"]
        del os.environ["DEVIN_DEFAULT_MODEL"]