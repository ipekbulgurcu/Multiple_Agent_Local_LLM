from langgraph.graph import StateGraph, END
from app.agents.nodes import (
    AgentState, 
    supervisor_node, 
    research_node, 
    code_node, 
    rag_node
)

# 1. Create the Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("Supervisor", supervisor_node)
workflow.add_node("Researcher", research_node)
workflow.add_node("Coder", code_node)
workflow.add_node("RAG_Expert", rag_node)

# 3. Add Edges (Routing Logic)
# From Supervisor, we go to the node decided in 'next', or END if FINISH.
workflow.add_conditional_edges(
    "Supervisor",
    lambda state: state["next"],
    {
        "Researcher": "Researcher",
        "Coder": "Coder",
        "RAG_Expert": "RAG_Expert",
        "FINISH": END
    }
)

# From Agents, we go back to Supervisor (to report results and get next step)
workflow.add_edge("Researcher", "Supervisor")
workflow.add_edge("Coder", "Supervisor")
workflow.add_edge("RAG_Expert", "Supervisor")

# 4. Set Entry Point
workflow.set_entry_point("Supervisor")

# 5. Compile
graph = workflow.compile()
