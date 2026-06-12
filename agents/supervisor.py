# agents/supervisor.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from state import ResearchState
from config import (
    OPENROUTER_API_KEY, OPENROUTER_BASE_URL,
    MAIN_MODEL, MAX_ITERATIONS
)

llm = ChatOpenAI(
    model=MAIN_MODEL,
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base=OPENROUTER_BASE_URL,
    temperature=0
)

# Structured output — supervisor returns typed JSON
class SupervisorOutput(BaseModel):
    next_agent: str = Field(
        description="One of: web_agent, rag_agent, code_agent, report_agent, FINISH"
    )
    reasoning: str = Field(description="Why this agent in one sentence")
    subtask: str = Field(description="Specific instruction for the agent")

parser = JsonOutputParser(pydantic_object=SupervisorOutput)

prompt = ChatPromptTemplate.from_template("""
You are a supervisor managing a research system.
Decide which agent acts next.

Agents available:
- web_agent: searches internet for current info
- rag_agent: searches internal knowledge base
- code_agent: writes or explains Python code
- report_agent: writes final report
- FINISH: after report is written

Query: {query}
Iteration: {iteration}/{max_iter}
Work done: {work_done}

Rules:
1. Research queries: web_agent first, then rag_agent
2. Code queries: rag_agent first, then code_agent
3. Always end with report_agent then FINISH
4. If iteration >= max: go to report_agent immediately

{format_instructions}
""")

def supervisor_node(state: ResearchState) -> dict:
    print(f"\n{'='*40}")
    print(f"SUPERVISOR — iteration {state['iteration_count']}")

    # Format what's been done
    work = []
    if state["web_search_results"]:
        work.append("Web search: done")
    if state["rag_results"]:
        work.append("Knowledge base: done")
    if state["generated_code"]:
        work.append("Code: generated")
    if state["draft_report"]:
        work.append("Report: drafted")
    
    work_str = "\n".join(work) if work else "Nothing yet"

    chain = prompt | llm | parser

    decision = chain.invoke({
        "query": state["user_query"],
        "iteration": state["iteration_count"],
        "max_iter": MAX_ITERATIONS,
        "work_done": work_str,
        "format_instructions": parser.get_format_instructions()
    })

    print(f"Next: {decision['next_agent']}")
    print(f"Why: {decision['reasoning']}")

    return {
        "next_agent": decision["next_agent"],
        "supervisor_reasoning": decision["reasoning"],
        "iteration_count": state["iteration_count"] + 1
    }