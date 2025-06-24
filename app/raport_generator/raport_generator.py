from app.agent.agent_state import AgentState


async def generate_report(state: AgentState) -> dict:
    """
    Generates a human-readable markdown report from the structured analysis.
    """
    analysis_result = state.get("analysis")
    # console.print(analysis_result)
    if not analysis_result or not analysis_result.bug_reports:
        return {"report": "No significant issues found that require a report."}

    log_file_name = state.get("log_file_path")
    report_parts = [f"# AI Tester Analysis for: `{log_file_name}`"]

    summary_points = []
    for report in analysis_result.bug_reports:
        summary_points.append(
            f"- **{report.severity} Severity**: {report.issue_summary}"
        )

    report_parts.append("## Summary of Findings")
    report_parts.append("\n".join(summary_points))
    report_parts.append("\n---")

    report_parts.append("## Detailed Bug Reports")
    for i, report in enumerate(analysis_result.bug_reports, 1):
        report_parts.append(f"### {i}. {report.issue_summary}")
        report_parts.append(f"- **Severity**: {report.severity}")
        report_parts.append(f"- **Timestamp**: `{report.timestamp}`")
        if report.file_path and report.line_number:
            report_parts.append(
                f"- **Location**: `{report.file_path}` at line `{report.line_number}`"
            )
        report_parts.append(f"- **Log Details**: `{report.log_details}`")
        report_parts.append("- **Path to Reproduce**:")
        for step in report.path_to_reproduce:
            report_parts.append(f"  - {step}")
        report_parts.append("")  # Add a newline for spacing

    final_report = "\n\n".join(report_parts)
    return {"report": final_report}
