from async_typer import AsyncTyper

from app.cli import analyze

# Create a Typer App instance. This is the standard way to build a robust CLI.
app = AsyncTyper()

# Register the 'analyze' function as a command.
# Typer is smart enough to see that 'analyze' is an async function
# and will handle running it correctly.
app.async_command()(analyze)


if __name__ == "__main__":
    # When this is called, Typer takes over, parses command-line arguments,
    # and executes the appropriate command with a proper async event loop.
    app()
