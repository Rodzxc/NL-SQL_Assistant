from langgraph.graph import MessagesState, StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage
from .tools.sql_tool import sql_tool
from .llm import llm
from .memory import memory_checkpointer
from functools import lru_cache

@lru_cache(maxsize=1)
def get_graph():
    # === Construcción del grafo ===
    graph_builder = StateGraph(MessagesState)

    # 1. Nodo LLM
    def query_or_respond(state: MessagesState):
        system_message_content = (
            "Sos un asistente experto. Respondé preguntas o usá herramientas si es necesario. "
            "Usá `sql_tool` para acceder a la base de datos. "
            "No inventes información ni resultados."
        )
        prompt = [SystemMessage(system_message_content)] + state["messages"]
        llm_with_tools = llm.bind_tools([sql_tool])
        response = llm_with_tools.invoke(prompt)
        return {"messages": [response]}

    # 2. Tool
    SQuirreL = ToolNode([sql_tool])

    # 3. Estructura del grafo
    graph_builder.add_node(query_or_respond)
    graph_builder.add_node('SQuirreL', SQuirreL)

    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond", tools_condition, {END: END, "SQuirreL": "SQuirreL"}
    )
    graph_builder.add_edge("SQuirreL", END)

    # 4. Compilar con memoria
    with memory_checkpointer() as checkpointer:
        return graph_builder.compile(checkpointer=checkpointer)