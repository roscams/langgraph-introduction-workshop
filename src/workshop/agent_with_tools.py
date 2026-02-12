"""Agent with Tools - Demonstrates tool usage with prebuilt create_agent"""

import math
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent


# Define tools
@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression.

    Args:
        expression: A mathematical expression to evaluate (e.g., '2 + 2', 'sqrt(16)')
    """
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith('_')}
        allowed_names['abs'] = abs
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: The name of the city to get weather for
    """
    weather_data = {
        "new york": "Sunny, 72°F (22°C)",
        "london": "Cloudy, 59°F (15°C)",
        "tokyo": "Rainy, 68°F (20°C)",
        "sydney": "Clear, 77°F (25°C)",
        "paris": "Partly cloudy, 64°F (18°C)",
        "amsterdam": "Rainy, 55°F (13°C)",
    }
    return weather_data.get(city.lower(), f"Weather data not available for {city}")


@tool
def search_knowledge_base(query: str) -> str:
    """Search the internal knowledge base for information.

    Args:
        query: The search query
    """
    kb = {
        "refund": "Refunds are available within 30 days of purchase with receipt.",
        "hours": "We're open Monday-Friday 9am-5pm EST.",
        "contact": "Email: support@example.com, Phone: 1-800-EXAMPLE",
        "shipping": "Free shipping on orders over $50. Standard delivery 3-5 business days.",
        "returns": "Returns accepted within 30 days. Items must be unused and in original packaging.",
    }

    for key, value in kb.items():
        if key in query.lower():
            return value
    return "No relevant information found. Try searching for: refund, hours, contact, shipping, returns"


# Setup tools and LLM
tools = [calculator, get_weather, search_knowledge_base]
llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

# Build the agent using prebuilt create_agent
# This replaces ~20 lines of manual StateGraph construction
graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""You are a helpful assistant with access to tools.
Use the calculator for math, get_weather for weather queries,
and search_knowledge_base for company information.""",
)
