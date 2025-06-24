from pathlib import Path

import pandas as pd
import typer
from rich.console import Console
from rich.markdown import Markdown

from app.agent.agent import create_graph

console = Console()


# Default log file path in project test data directory
default_file = str(Path("tests/test_data/dummy_log.txt"))


async def analyze(
    log_file_path: str = typer.Argument(
        default_file, help="The path to the log file to be analyzed."
    ),
):
    """
    Analyzes a log file to find bugs, generates a report, and suggests areas of focus.
    """
    console.print(f":mag: Analyzing log file: [bold cyan]{log_file_path}[/bold cyan]")
    agent = create_graph()
    inputs = {"log_file_path": log_file_path}
    final_state = {}

    with console.status("[bold green]Agent at work...[/bold green]") as status:
        # Use astream_events (v2) for robust, detailed streaming.
        async for event in agent.astream_events(
            inputs, version="v2", stream_mode="values"
        ):
            kind = event["event"]
            if kind == "on_chain_start":
                if event["name"] != "__end__":
                    status.update(
                        spinner="dots",
                        status=f"Running: [bold blue]{event['name']}[/bold blue]...",
                    )
            elif kind == "on_chain_end":
                if event["name"] == "parse_logs":
                    node_output = event["data"].get("output", {})
                    if isinstance(node_output, dict):
                        parsed_logs_df = node_output.get("parsed_logs")
                        if (
                            isinstance(parsed_logs_df, pd.DataFrame)
                            and not parsed_logs_df.empty
                        ):
                            console.print("\n--- Parsed Log Entries ---")
                            console.print(parsed_logs_df.to_string())
                            console.print("--------------------------\n")
                if event["name"] == "generate_report":  # this is last step on chain
                    final_state = event["data"]["output"]

    report = final_state.get("report")
    if report and "No significant issues" not in report:
        console.print("\n\n--- [bold green]Analysis Report[/bold green] ---")
        console.print(Markdown(report))
        console.print("--- [bold green]End of Report[/bold green] ---")
    else:
        console.print("\n[bold red]Could not generate a report.[/bold red]")
        analysis = final_state.get("analysis", "No analysis available.")
        console.print("\n--- [bold yellow]Raw Analysis[/bold yellow] ---")
        console.print(analysis)
        console.print("--- [bold yellow]End of Raw Analysis[/bold yellow] ---")
