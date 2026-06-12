# You know this structure already:
workflow = StateGraph(ResearchState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("web", web_agent_node)
# ... add all nodes

workflow.set_entry_point("supervisor")

workflow.add_conditional_edges("supervisor", route_fn, {...})

workflow.add_edge("web", "supervisor")  # loop back
# ... all agents loop back

workflow.add_edge("report", "human_review")
workflow.add_conditional_edges("human_review", approval_fn, {...})
workflow.add_edge("finalize", END)

checkpointer = MemorySaver()
graph = workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["human_review"]
)