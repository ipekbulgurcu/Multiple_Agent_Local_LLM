from typing import Annotated, Sequence, TypedDict, Union, List, Dict
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from app.agents.tools import get_web_search_tool, get_python_repl_tool, get_rag_tool
from app.models.llm import get_fast_llm, get_smart_llm
from langchain.output_parsers.json import SimpleJsonOutputParser
from app.core.logging import logger

# 1. Define State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    model_name: str

# 2. Define Tools
web_search_tool = get_web_search_tool()
python_repl_tool = get_python_repl_tool()
rag_tool = get_rag_tool()

# 3. Agents
def create_agent(llm: object, tools: list, system_prompt: str):
    """Helper to create an agent."""
    # We can use create_react_agent from langgraph prebuilt for simplicity
    # or build a specific chain.
    # For Researcher/Coder/RAG, they are standard ReAct agents or similar.
    return create_react_agent(llm, tools, state_modifier=system_prompt)

# --- Nodes ---

def research_node(state: AgentState):
    """
    Web Researcher Agent Node.
    """
    logger.info("Node Triggered: Researcher")
    try:
        model_name = state.get("model_name")
        agent = create_agent(
            get_smart_llm(model_name), 
            [web_search_tool], 
            "You are a web researcher. Search the internet for information."
        )
        result = agent.invoke(state)
        return {"messages": [result["messages"][-1]]}
    except Exception as e:
        logger.error(f"Researcher Error: {e}")
        return {"messages": [HumanMessage(content=f"Error in Researcher Agent: {str(e)}")]}

def code_node(state: AgentState):
    """
    Code Interpreter Agent Node.
    """
    logger.info("Node Triggered: Coder")
    try:
        model_name = state.get("model_name")
        agent = create_agent(
            get_smart_llm(model_name),
            [python_repl_tool],
            "You are a python expert. Write and execute code to solve problems."
        )
        result = agent.invoke(state)
        return {"messages": [result["messages"][-1]]}
    except Exception as e:
        logger.error(f"Coder Error: {e}")
        return {"messages": [HumanMessage(content=f"Error in Coder Agent: {str(e)}")]}

def rag_node(state: AgentState):
    """
    Document Expert (RAG) Agent Node.
    """
    logger.info("Node Triggered: RAG_Expert")
    try:
        model_name = state.get("model_name")
        agent = create_agent(
            get_smart_llm(model_name),
            [rag_tool],
            "You are a document expert. Use the rag_tool to retrieve information from the knowledge base."
        )
        result = agent.invoke(state)
        return {"messages": [result["messages"][-1]]}
    except Exception as e:
        logger.error(f"RAG Error: {e}")
        return {"messages": [HumanMessage(content=f"Error in RAG Agent: {str(e)}")]}

def supervisor_node(state: AgentState):
    """
    Supervisor Node (Router).
    Decides which agent to call next or if the task is finished.
    Uses 'Fast Model'.
    """
    logger.info("Node Triggered: Supervisor")
    llm = get_fast_llm()
    
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        " following workers: [Researcher, Coder, RAG_Expert].\n"
        "Given the following user request, respond with the worker to act next."
        " Each worker will perform a task and respond with their results and status."
        " When finished, respond with FINISH.\n"
        "Respond in JSON format: {{'next': 'WorkerName'}} or {{'next': 'FINISH'}}"
    )
    
    messages = state["messages"]
    # We might need to format messages for the router prompt
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Who should act next? Return ONLY the JSON.")
    ])
    
    chain = prompt | llm | SimpleJsonOutputParser()
    
    # Try to parse the result, handle potential errors (or let it fail)
    try:
        result = chain.invoke({"messages": messages})
    except Exception as e:
        # Fallback if JSON parsing fails or model hallucinates
        # For robustness, maybe default to FINISH or ask clarification, 
        # but here we'll retry or just return FINISH to be safe.
        print(f"Router Error: {e}")
        return {"next": "FINISH"}

    return {"next": result.get("next", "FINISH")}
