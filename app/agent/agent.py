from langgraph.graph import END, StateGraph

from app.agent.agent_state import AgentState
from app.analyzer.analyzer import analyze_logs
from app.parser.parser import parse_log_file
from app.raport_generator.raport_generator import generate_report


def create_graph():
    """
    Creates and compiles the LangGraph agent. The graph can handle async nodes.
    """
    workflow = StateGraph(AgentState)

    # Add the nodes
    workflow.add_node("parse_logs", parse_log_file)
    workflow.add_node("analyze_logs", analyze_logs)
    workflow.add_node("generate_report", generate_report)

    # Set the entry point
    workflow.set_entry_point("parse_logs")

    # Add edges
    workflow.add_edge("parse_logs", "analyze_logs")
    workflow.add_edge("analyze_logs", "generate_report")
    workflow.add_edge("generate_report", END)

    # Compile the graph
    app = workflow.compile()
    return app
