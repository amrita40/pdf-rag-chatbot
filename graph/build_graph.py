from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict, Annotated

# Your custom nodes
from .nodes import (
    router,
    retrieval_node,
    grade_retrieval_node,
    rewrite_node,
    web_search_node,
    generate_answer,
    grade_answer,
)

# Step 1: Define the State Schema
class GraphState(TypedDict):
    question: str
    docs: list
    answer: str
    relevance: str
    answer_quality: str

# Step 2: Wrap condition functions in RunnableLambda
def route_to_vectorstore(state: GraphState):
    return "vectorstore" if "pdf" in state["question"].lower() else "web_search"

def grade_retrieval_decision(state: GraphState):
    # Use the 'relevance' key returned by check_relevance in nodes.py
    return "relevant" if "relevant" in state.get("relevance", "").lower() else "irrelevant"

def grade_answer_decision(state: GraphState):
    # Use the 'answer_quality' key returned by check_answer_quality in nodes.py
    return "correct" if "correct" in state.get("answer_quality", "").lower() else "incorrect"

# Step 3: Build the Graph
def get_graph():
    builder = StateGraph(GraphState)

    # Add Nodes
    builder.add_node("router", router)
    builder.add_node("vectorstore", retrieval_node)
    builder.add_node("grade_retrieval", grade_retrieval_node)
    builder.add_node("rewrite", rewrite_node)
    builder.add_node("web_search", web_search_node)
    builder.add_node("generate", generate_answer)
    builder.add_node("grade_answer", grade_answer)

    # Entry Point
    builder.set_entry_point("router")

    # Conditional Routing from router
    builder.add_conditional_edges(
        "router",
        RunnableLambda(route_to_vectorstore),
        {
            "vectorstore": "vectorstore",
            "web_search": "web_search",
        },
    )

    # Vectorstore path
    builder.add_edge("vectorstore", "grade_retrieval")
    builder.add_conditional_edges(
        "grade_retrieval",
        RunnableLambda(grade_retrieval_decision),
        {
            "relevant": "generate",
            "irrelevant": "rewrite",
        },
    )
    builder.add_edge("rewrite", "vectorstore")

    # Web search path
    builder.add_edge("web_search", "generate")

    # Answer grading
    builder.add_edge("generate", "grade_answer")
    builder.add_conditional_edges(
        "grade_answer",
        RunnableLambda(grade_answer_decision),
        {
            "correct": END,
            "incorrect": "rewrite",
        },
    )

    return builder.compile()
