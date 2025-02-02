from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, field_validator
import keyring
from rich import print as rprint

class DevinSettings(BaseSettings):
    """Settings for Devin CLI."""
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='DEVIN_',
        case_sensitive=False
    )
    
    api_key: Optional[SecretStr] = None
    project_path: Optional[Path] = None
    default_model: str = "gpt-4"
    max_tokens: int = 4096
    temperature: float = 0.7
    
    @classmethod
    def load(cls):
        """Load settings from environment variables and .env file."""
        return cls()
    
    @field_validator('api_key')
    def validate_api_key(cls, v):
        """Validate API key format."""
        if v and len(v.get_secret_value()) < 8:  # Relaxed validation for testing
            raise ValueError("API key seems too short")
        return v

    def save(self):
        """Save current settings to .env file and secure storage."""
        env_content = []
        for field, value in self:
            if value is not None:
                if isinstance(value, SecretStr):
                    # Store API key in system keyring
                    keyring.set_password("devin-cli", "api_key", value.get_secret_value())
                    continue  # Skip storing in .env
                env_content.append(f"DEVIN_{field.upper()}={value}")
        
        with open('.env', 'w') as f:
            f.write('\n'.join(env_content))
        for field, value in self:
            if value is not None:
                rprint(f"Set {field} to {value if not isinstance(value, SecretStr) else '********'}")
        rprint(f"[green]✓[/green] Configuration saved successfully")
        if any(isinstance(value, SecretStr) for field, value in self):
            rprint(f"[green]✓[/green] API key has been securely stored")

    @classmethod
    def load(cls):
        """Load settings from environment variables, .env file, and secure storage."""
        settings = cls()
        
        # Try to load API key from keyring if not set in env
        if not settings.api_key:
            stored_key = keyring.get_password("devin-cli", "api_key")
            if stored_key:
                settings.api_key = SecretStr(stored_key)
        
        return settings