from langchain_core.messages import HumanMessage, SystemMessage
from rich.console import Console

from app.agent.agent_state import AgentState, AnalysisResult
from app.llm.llm import create_llm

console = Console()


async def analyze_logs(state: AgentState) -> dict:
    """
    Analyzes log slices around errors to produce structured bug reports.
    """
    parsed_logs = state.get("parsed_logs")
    if parsed_logs is None or parsed_logs.empty:
        return {"analysis": AnalysisResult(bug_reports=[])}

    # Find indices of critical/error logs
    error_indices = parsed_logs[
        parsed_logs["log_level"].isin(["ERROR", "CRITICAL", "WARNING"])
    ].index

    if error_indices.empty:
        return {"analysis": AnalysisResult(bug_reports=[])}

    analyzer_llm = create_llm()
    structured_llm = analyzer_llm.with_structured_output(AnalysisResult)

    initial_bug_reports = []
    processed_indices = set()

    for idx in error_indices:
        if idx in processed_indices:
            continue

        start = max(0, idx - 20)
        end = min(len(parsed_logs), idx + 5)
        log_window = parsed_logs.iloc[start:end]

        for i in log_window[
            log_window["log_level"].isin(["ERROR", "CRITICAL", "WARNING"])
        ].index:
            processed_indices.add(i)

        log_summary = log_window.to_json(orient="records", lines=True)

        system_prompt = """You are a Senior QA Engineer. Your task is to analyze a slice of log entries and produce a single, structured bug report for the primary error.
The logs are in JSON Lines format. Your goal is to extract key details from the log and traceback.

Based on the logs, formulate a clear "Path to Reproduce". For traceback errors, extract the file path and line number.
Estimate the severity of the bug (High, Medium, or Low).

Respond ONLY with the structured JSON requested."""

        human_prompt = f"""Please analyze the following log data slice and generate a bug report for the main error.
---
{log_summary}
---"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt),
            ]
            response = await structured_llm.ainvoke(messages)
            if response.bug_reports:
                initial_bug_reports.extend(response.bug_reports)
        except Exception as e:
            console.print(f"Error analyzing log slice near index {idx}: {e}")

    # --- Semantic Deduplication Step ---
    if len(initial_bug_reports) <= 1:
        return {"analysis": AnalysisResult(bug_reports=initial_bug_reports)}

    deduplicator_llm = create_llm().with_structured_output(AnalysisResult)

    reports_json = "\n".join([report.json() for report in initial_bug_reports])

    dedup_system_prompt = """You are a bug report analysis expert. Your task is to read a list of bug reports in JSON format and identify semantic duplicates.
Some reports might describe the exact same underlying problem with slightly different wording.
Merge the duplicate reports into a single, high-quality report. Choose the best-written summary and path to reproduce from the duplicates.
Return a final, deduplicated list of bug reports in the same JSON structure."""

    dedup_human_prompt = (
        f"""Please deduplicate the following bug reports:\n{reports_json}"""
    )

    try:
        dedup_messages = [
            SystemMessage(content=dedup_system_prompt),
            HumanMessage(content=dedup_human_prompt),
        ]
        final_analysis = await deduplicator_llm.ainvoke(dedup_messages)
        return {"analysis": final_analysis}
    except Exception as e:
        console.print(f"Error during bug report deduplication: {e}")
        # Fallback to returning the original list if deduplication fails
        return {"analysis": AnalysisResult(bug_reports=initial_bug_reports)}
