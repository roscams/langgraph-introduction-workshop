"""Simple Chatbot Graph for LangGraph Studio Demo"""

from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage


# Use prebuilt MessagesState instead of custom TypedDict
# MessagesState already includes: messages: Annotated[list, add_messages]
class ChatState(MessagesState):
    """State for the chatbot graph - extends prebuilt MessagesState"""
    pass


# Initialize the LLM
llm = ChatOpenAI(model="gpt-5-mini", temperature=0.7)


def chatbot(state: ChatState) -> dict:
    """Process messages and generate a response"""
    messages = [
        SystemMessage(content="You are a helpful assistant. Be concise and friendly."),
        *state["messages"]
    ]
    response = llm.invoke(messages)
    return {"messages": [response]}


# Build the graph
builder = StateGraph(ChatState)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# Compile the graph (langgraph dev handles persistence automatically)
graph = builder.compile()
