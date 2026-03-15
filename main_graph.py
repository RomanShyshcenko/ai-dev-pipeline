import json

from langgraph.graph import END, StateGraph

from agents.gatekeeper_agent import run_gatekeeper
from core.state import AgentState

workflow = StateGraph(AgentState)
workflow.add_node("gatekeeper", run_gatekeeper)
workflow.set_entry_point("gatekeeper")
workflow.add_edge("gatekeeper", END)

app = workflow.compile()


if __name__ == "__main__":
    bad_task = (
        "Build a feature to upload a CSV of contacts and process it. "
        "Just make it work quickly."
    )

    initial_state = {
        "raw_tt": bad_task,
        "messages": [],
    }

    result = app.invoke(initial_state)
    decision = result["gatekeeper_decision"]

    print("\n=== Gatekeeper Decision ===")
    print(json.dumps(decision.model_dump(), indent=2))
