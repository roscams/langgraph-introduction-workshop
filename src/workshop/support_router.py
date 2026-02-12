"""Support Router Graph - Routes queries to specialized handlers"""

from typing import Literal
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


# Use prebuilt MessagesState and extend with additional fields
class SupportState(MessagesState):
    """State for the support router graph - extends prebuilt MessagesState"""
    query_type: str


llm = ChatOpenAI(model="gpt-5-mini", temperature=0)


def classify_query(state: SupportState) -> dict:
    """Classify the user's query into a category"""
    last_message = state["messages"][-1].content

    response = llm.invoke([
        SystemMessage(content="""Classify the user query into one of these categories:
        - billing: Questions about payments, invoices, subscriptions
        - technical: Technical issues, bugs, how-to questions
        - general: Everything else

        Respond with ONLY the category name (billing, technical, or general)."""),
        HumanMessage(content=last_message)
    ])

    query_type = response.content.strip().lower()
    # Ensure valid category
    if query_type not in ["billing", "technical", "general"]:
        query_type = "general"

    return {"query_type": query_type}


def billing_handler(state: SupportState) -> dict:
    """Handle billing-related queries"""
    response = llm.invoke([
        SystemMessage(content="""You are a billing specialist. Help with payment and subscription issues.
        Be professional and provide clear information about billing policies."""),
        *state["messages"]
    ])
    return {"messages": [response]}


def technical_handler(state: SupportState) -> dict:
    """Handle technical queries"""
    response = llm.invoke([
        SystemMessage(content="""You are a technical support specialist. Help with bugs and technical issues.
        Provide step-by-step solutions when possible."""),
        *state["messages"]
    ])
    return {"messages": [response]}


def general_handler(state: SupportState) -> dict:
    """Handle general queries"""
    response = llm.invoke([
        SystemMessage(content="""You are a helpful customer support agent.
        Be friendly, professional, and helpful."""),
        *state["messages"]
    ])
    return {"messages": [response]}


def route_to_handler(state: SupportState) -> Literal["billing", "technical", "general"]:
    """Route to the appropriate handler based on query_type"""
    query_type = state.get("query_type", "general")
    if query_type == "billing":
        return "billing"
    elif query_type == "technical":
        return "technical"
    return "general"


# Build the graph
builder = StateGraph(SupportState)

# Add nodes
builder.add_node("classify", classify_query)
builder.add_node("billing", billing_handler)
builder.add_node("technical", technical_handler)
builder.add_node("general", general_handler)

# Add edges
builder.add_edge(START, "classify")
builder.add_conditional_edges(
    "classify",
    route_to_handler,
    {
        "billing": "billing",
        "technical": "technical",
        "general": "general"
    }
)
builder.add_edge("billing", END)
builder.add_edge("technical", END)
builder.add_edge("general", END)

# Compile the graph (langgraph dev handles persistence automatically)
graph = builder.compile()
