from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

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
    
    def save(self):
        """Save current settings to .env file."""
        env_content = []
        for field, value in self:
            if value is not None:
                if isinstance(value, SecretStr):
                    value = value.get_secret_value()
                env_content.append(f"DEVIN_{field.upper()}={value}")
        
        with open('.env', 'w') as f:
            f.write('\n'.join(env_content))