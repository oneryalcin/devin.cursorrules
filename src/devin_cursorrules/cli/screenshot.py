import typer
from rich import print
from pathlib import Path
from typing import Optional
from ..screenshot import take_screenshot_sync

app = typer.Typer(
    name="screenshot",
    help="Capture screenshots of web pages",
    no_args_is_help=True,
)

@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """Screenshot utilities for capturing web pages"""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()

@app.command()
def capture(
    url: str = typer.Argument(..., help="URL to capture"),
    output: str = typer.Option(
        None,
        "--output",
        "-o",
        help="Output path for the screenshot"
    ),
    width: int = typer.Option(
        1280,
        "--width",
        "-w",
        help="Viewport width"
    ),
    height: int = typer.Option(
        720,
        "--height",
        "-h",
        help="Viewport height"
    ),
    full_page: bool = typer.Option(
        True,
        "--full-page/--viewport-only",
        help="Capture full scrollable page or just viewport"
    ),
):
    """Capture a screenshot of a webpage"""
    try:
        print(f"[bold blue]Capturing screenshot of {url}...[/bold blue]")
        output_path = take_screenshot_sync(
            url=url,
            output_path=output,
            width=width,
            height=height,
            full_page=full_page
        )
        print(f"[bold green]Screenshot saved to:[/bold green] {output_path}")
    except ValueError as e:
        print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)
    except Exception as e:
        print(f"[bold red]Error:[/bold red] Failed to capture screenshot: {str(e)}")
        raise typer.Exit(1)