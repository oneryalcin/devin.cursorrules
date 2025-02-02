import typer
from rich import print
from typing import Optional
from pathlib import Path
from ..config import DevinSettings

config_app = typer.Typer(
    name="config",
    help="Manage Devin CLI configuration",
    no_args_is_help=True
)

@config_app.command("set")
def set_config(
    key: str = typer.Argument(..., help="Configuration key to set"),
    value: str = typer.Argument(..., help="Value to set for the key")
):
    """Set a configuration value"""
    settings = DevinSettings.load()
    
    try:
        if hasattr(settings, key):
            if key == 'project_path':
                value = str(Path(value).absolute())
            setattr(settings, key, value)
            settings.save()
            print(f"[green]✓[/green] Set {key} to {value}")
        else:
            print(f"[red]Error:[/red] Unknown configuration key: {key}")
            raise typer.Exit(1)
    except Exception as e:
        print(f"[red]Error:[/red] Failed to set configuration: {str(e)}")
        raise typer.Exit(1)

@config_app.command("get")
def get_config(
    key: Optional[str] = typer.Argument(None, help="Configuration key to get")
):
    """Get configuration value(s)"""
    settings = DevinSettings.load()
    
    if key:
        if hasattr(settings, key):
            value = getattr(settings, key)
            if value is None:
                print(f"{key}: [italic]not set[/italic]")
            else:
                if key == 'api_key' and value is not None:
                    print(f"{key}: {value.get_secret_value()}")
                else:
                    print(f"{key}: {value}")
        else:
            print(f"[red]Error:[/red] Unknown configuration key: {key}")
            raise typer.Exit(1)
    else:
        # Show all configuration values
        for field, value in settings:
            if value is None:
                print(f"{field}: [italic]not set[/italic]")
            else:
                if field == 'api_key' and value is not None:
                    print(f"{field}: {value.get_secret_value()}")
                else:
                    print(f"{field}: {value}")