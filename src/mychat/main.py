import typer
from dotenv import load_dotenv
from mychat.ui.cli import run_cli
from mychat.ui.web import run_web
import os

# Load environment variables
load_dotenv()

app = typer.Typer(help="MyChat CLI Tool", add_completion=False)

@app.command()
def cli():
    """Run the terminal chat interface."""
    run_cli()

@app.command()
def web():
    """Run the Gradio web interface."""
    run_web()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    MyChat Application.
    Default behavior is to run the CLI.
    """
    if ctx.invoked_subcommand is None:
        run_cli()

if __name__ == "__main__":
    app()
