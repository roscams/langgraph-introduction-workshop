# LangGraph Introduction Workshop

A hands-on 2-hour workshop covering LangGraph fundamentals and multi-agent orchestration.

## Prerequisites

- Python 3.10+
- Basic Python knowledge
- Familiarity with LLM concepts
- API keys (OpenAI and optionally Tavily for web search)

## Setup

1. **Clone or download this repository**

2. **Install dependencies with uv:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. **Start Jupyter:**
   ```bash
   uv run jupyter notebook
   ```

## Notebooks

1. **01_introduction_basic_graphs.ipynb**
   - What is LangGraph and when to use it
   - Core concepts: State, Nodes, Edges
   - Building a simple chatbot
   - Exercise: Build a joke generator

2. **02_conditional_routing.ipynb**
   - Conditional edges for dynamic routing
   - Intent-based routing patterns
   - Looping until conditions are met
   - Exercise: Build a content moderator

3. **03_tool_integration.ipynb**
   - Creating tools with `@tool` decorator
   - Binding tools to LLMs
   - The agent loop pattern
   - ToolNode for automatic execution
   - Exercise: Build a research assistant

4. **04_persistence_memory.ipynb**
   - MemorySaver for conversation history
   - Thread IDs for separate conversations
   - Inspecting and resuming state
   - Exercise: Build a personal assistant

5. **05_multi_agent_orchestration.ipynb**
   - Supervisor pattern
   - Agent teams with specialized workers
   - Hierarchical agents
   - Agent handoffs
   - Exercise: Build a content creation team

6. **06_langgraph_studio.ipynb**
   - What is LangGraph Studio
   - Project setup for Studio
   - Visual debugging and testing
   - Time travel debugging
   - Studio best practices

## LangGraph Studio

This workshop includes pre-configured graphs for LangGraph Studio:

### Quick Start

```bash
# Install the CLI (if not already installed)
pip install "langgraph-cli[inmem]"

# Start Studio
cd langgraph-introduction-workshop
langgraph dev

```

### Available Graphs in Studio

| Graph | Description |
|-------|-------------|
| `chatbot` | Simple conversational chatbot with memory |
| `support_router` | Routes queries to billing/technical/general handlers |
| `agent_with_tools` | Agent with calculator, weather, and search tools |
| `multi_agent_team` | Supervisor with researcher, coder, and writer agents |

### Project Structure for Studio

```
langgraph-introduction-workshop/
├── langgraph.json          # Studio configuration
├── .env                    # API keys
└── src/workshop/           # Graph modules
    ├── chatbot.py
    ├── support_router.py
    ├── agent_with_tools.py
    └── multi_agent_team.py
```

## Key Concepts Covered

- **StateGraph**: The main graph builder
- **TypedDict State**: Defining what data flows through the graph
- **add_messages**: Annotation for message accumulation
- **Conditional Edges**: Dynamic routing based on state
- **ToolNode**: Automatic tool execution
- **MemorySaver**: In-memory checkpointing
- **Supervisor Pattern**: Central coordinator with worker agents
- **LangGraph Studio**: Visual IDE for debugging and testing

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangGraph Studio](https://studio.langchain.com/) - Visual IDE for LangGraph
- [LangSmith](https://smith.langchain.com/) - For production monitoring
- [LangChain Documentation](https://python.langchain.com/)

## Troubleshooting

### API Key Issues
Make sure your `.env` file has valid API keys:
```
OPENAI_API_KEY=sk-...
```

### Import Errors
Ensure you've installed all dependencies:
```bash
uv sync
```

### Graph Visualization Not Working
Graph visualization requires `pygraphviz` or will fall back to mermaid. If images don't render, the code will still work.

## License

MIT

## link
https://tundra-thief-3b2.notion.site/API-key-3064578ac6e8808aa271db12f8fe44ed
