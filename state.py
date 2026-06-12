# state.py
from typing import TypedDict, List, Annotated, Optional
from langchain_core.messages import BaseMessage
import operator

class ResearchState(TypedDict):
    # INPUT — never changes
    user_query: str
    task_type: str

    # MEMORY — appended each turn
    messages: Annotated[List[BaseMessage], operator.add]

    # AGENT RESULTS — appended by each agent
    agent_findings: Annotated[List[str], operator.add]
    web_search_results: Annotated[List[str], operator.add]
    rag_results: Annotated[List[str], operator.add]

    # CODE OUTPUT — replaced (only one code block)
    generated_code: str
    code_explanation: str
    code_language: str

    # SUPERVISOR CONTROL — replaced each iteration
    next_agent: str
    supervisor_reasoning: str
    iteration_count: int

    # HUMAN IN LOOP — replaced by human decision
    draft_report: str
    human_approved: bool
    human_feedback: str

    # FINAL OUTPUT
    final_report: str