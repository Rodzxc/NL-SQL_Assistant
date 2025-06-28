import streamlit as st
from streamlit_utils.response_streamlit import sql_query_response, chain_response
import secrets

# === Guardar el grafo y responder ===
def build_response(txt: str):
    if "graph" not in st.session_state:
        from chain.chain import get_graph
        st.session_state.graph = get_graph()

    graph = st.session_state.graph 

    # --- Limites ---
    forbidden_keywords = ["drop", "update", "delete", "create", "insert", "alter", "truncate"]
    if any(k in txt.strip().lower() for k in forbidden_keywords):
        st.error("Sorigordi. No se permite alterar la base de datos.")

    # --- respuesta consulta SQL ---
    elif txt.strip().lower().startswith("select"):
        sql_query_response(txt)

    # --- respuesta LLM ---
    else:
        st.session_state["messages"].append({"role": "user", "content": txt})

        if "thread_id" not in st.session_state:
            short_id = str(secrets.token_hex(4))
            st.session_state.thread_id = str(short_id)

        config = {"configurable": {"thread_id": st.session_state.thread_id}}

        with st.spinner("Pensando..."):

            try:
                for step in graph.stream(
                    {"messages": st.session_state["messages"]},
                    stream_mode="values",
                    config=config,
                ):
                    if "messages" in step and step["messages"]:
                        rsp = step["messages"][-1]
                        if hasattr(rsp, "type"):
                            if rsp.type.title() == 'Human':
                                st.markdown(f"**🧑 Usuario:** {rsp.content}")
                            
                            chain_response(rsp)
            
            except Exception as e:
                st.error(f"Error en el 'asistente IA graph.stream': {e}")