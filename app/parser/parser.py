import re
from collections import namedtuple
from pathlib import Path

import aiofiles
import pandas as pd
import yaml
from rich.console import Console

from app.agent.agent_state import AgentState

console = Console()

# A robust regex for a common log format: [TIMESTAMP] [LEVEL] [COMPONENT] Message
# Example: [2024-07-29 10:00:00,123] [INFO] [AuthService] User 'admin' logged in successfully.


# Load settings.yaml
with open(Path("config/settings.yaml"), "r") as f:
    config = yaml.safe_load(f)

log_format = config["log"]["format"]
structure = config["log"]["structure"]

fields = list(structure.keys())  # e.g., ["timestamp", "log_level", "component", "message"]

# Dynamically create LogEntry
LogEntry = namedtuple("LogEntry", fields)

log_pattern = re.compile(log_format)


async def parse_log_file(state: AgentState) -> dict:
    """
    Reads and parses the log file asynchronously into a structured DataFrame.
    """
    log_file_path = state["log_file_path"]
    log_entries = []

    try:
        async with aiofiles.open(log_file_path, "r", encoding="utf-8") as f:
            async for line in f:
                match = log_pattern.search(line.strip())
                if match:
                    entry_data = match.groupdict()
                    log_entries.append(LogEntry(**entry_data))
                elif log_entries:
                    last_entry = log_entries[-1]
                    updated_message = f"{last_entry.message}\\n{line.strip()}"
                    log_entries[-1] = last_entry._replace(message=updated_message)
                else:
                    console.print(
                        f"Warning: Skipping unmatched log line: {line.strip()}"
                    )

        if not log_entries:
            return {"parsed_logs": pd.DataFrame()}

        df = pd.DataFrame(log_entries)
        return {"parsed_logs": df}

    except FileNotFoundError:
        console.print(f"Error: Log file not found at {log_file_path}")
        return {"parsed_logs": None}
    except Exception as e:
        console.print(f"Error reading or parsing log file: {e}")
        return {"parsed_logs": None}
