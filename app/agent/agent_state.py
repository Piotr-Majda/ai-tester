from typing import List, Optional, TypedDict

import pandas as pd
from pydantic import BaseModel, Field


# --- Pydantic Models for Structured Output ---
class BugReport(BaseModel):
    issue_summary: str = Field(
        description="A concise, one-sentence summary of the bug."
    )
    severity: str = Field(
        description="The severity of the bug (e.g., 'High', 'Medium', 'Low')."
    )
    log_details: str = Field(
        description="The full, exact log message of the critical error."
    )
    timestamp: str = Field(description="The full timestamp of the critical error log.")
    file_path: Optional[str] = Field(
        description="The source file path from the traceback, if available."
    )
    line_number: Optional[int] = Field(
        description="The line number from the traceback, if available."
    )
    path_to_reproduce: List[str] = Field(
        description="A numbered list of user or system actions that led to the error."
    )


class AnalysisResult(BaseModel):
    """A list of bug reports found in the logs."""

    bug_reports: List[BugReport]


class AgentState(TypedDict):
    """
    Represents the state of our agent.
    """

    log_file_path: str
    parsed_logs: Optional[pd.DataFrame]
    analysis: Optional[AnalysisResult]  # Changed from str to structured data
    report: Optional[str]
