import typer
from rich import print
from pathlib import Path
from typing import Optional
from importlib.metadata import version as get_version, PackageNotFoundError
from .config import config_app
from .screenshot import app as screenshot_app

app = typer.Typer(
    name="devin",
    help="Devin-like AI assistant capabilities for your development workflow",
    no_args_is_help=True,  # This ensures help is shown when no arguments are provided
)

# Add sub-commands
app.add_typer(config_app)
app.add_typer(screenshot_app)

def version_callback(value: bool):
    if value:
        try:
            version = get_version('devin-cursorrules')
        except PackageNotFoundError:
            version = "0.1.0"  # Default version from pyproject.toml
        print(f"[bold green]devin-cli[/bold green] version: {version}")
        raise typer.Exit()

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version and exit", callback=version_callback
    ),
):
    """Devin CLI - AI assistant capabilities for your development workflow"""
    if ctx.invoked_subcommand is None and not version:
        typer.echo(ctx.get_help())
        raise typer.Exit()

@app.command()
def init(
    path: str = typer.Argument(".", help="Path to initialize Devin"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing files"),
):
    """Initialize a new project with Devin capabilities"""
    project_path = Path(path).absolute()
    cursorrules_path = project_path / ".cursorrules"
    
    if cursorrules_path.exists() and not force:
        print("[red]Error:[/red] .cursorrules already exists. Use --force to overwrite.")
        raise typer.Exit(1)
    
    try:
        cursorrules_content = """# Instructions\n\n# Tools\n\n# Lessons\n\n# Scratchpad\n"""
        cursorrules_path.write_text(cursorrules_content)
        print(f"[green]✓[/green] Created {cursorrules_path}")
        print("[green]Successfully initialized Devin![/green]")
    except Exception as e:
        print(f"[red]Error:[/red] Failed to initialize Devin: {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()