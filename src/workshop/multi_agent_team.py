"""Multi-Agent Team - Supervisor pattern using prebuilt create_supervisor"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph_supervisor import create_supervisor


# Initialize LLM
llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

# Create specialized worker agents using create_agent
researcher = create_agent(
    model=llm,
    tools=[],  # Could add research-specific tools here
    system_prompt="""You are a research specialist.
Provide accurate, well-researched information.
Be concise but thorough. Cite sources when possible.""",
    name="researcher",
)

coder = create_agent(
    model=llm,
    tools=[],  # Could add coding-specific tools here
    system_prompt="""You are a coding specialist.
Write clean, well-commented code.
Explain your implementation choices.""",
    name="coder",
)

writer = create_agent(
    model=llm,
    tools=[],  # Could add writing-specific tools here
    system_prompt="""You are a writing specialist.
Create clear, engaging, well-structured content.
Adapt your style to the task.""",
    name="writer",
)

# Create supervisor using prebuilt create_supervisor
# This replaces ~80 lines of manual graph construction
graph = create_supervisor(
    model=llm,
    agents=[researcher, coder, writer],
    prompt=(
        "You are a supervisor managing a team of specialists:\n"
        "- researcher: Expert at finding information, analyzing data, and providing facts\n"
        "- coder: Expert at writing, reviewing, and explaining code\n"
        "- writer: Expert at writing, editing, and formatting text content\n\n"
        "Based on the user's request, decide which specialist should handle the task.\n"
        "You can assign work to multiple specialists sequentially if needed.\n"
        "Do not do any work yourself - always delegate to the appropriate specialist."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()
