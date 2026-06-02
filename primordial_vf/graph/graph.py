from __future__ import annotations

from langgraph.graph import END, StateGraph

from primordial_vf.graph.nodes.compile_context import compile_context_node
from primordial_vf.graph.nodes.retrieve_style import retrieve_style_node
from primordial_vf.graph.nodes.synthesize import synthesize_node
from primordial_vf.graph.nodes.validate_input import validate_input_node
from primordial_vf.graph.state import VFState


def build_graph():
    """Build the style transformation graph."""
    graph = StateGraph(VFState)

    graph.add_node("validate_input", validate_input_node)
    graph.add_node("retrieve_style", retrieve_style_node)
    graph.add_node("compile_context", compile_context_node)
    graph.add_node("synthesize", synthesize_node)

    graph.set_entry_point("validate_input")
    graph.add_edge("validate_input", "retrieve_style")
    graph.add_edge("retrieve_style", "compile_context")
    graph.add_edge("compile_context", "synthesize")
    graph.add_edge("synthesize", END)

    return graph.compile()