import streamlit as st
from streamlit_utils.layout import set_background, show_header
from streamlit_utils.autocomplete_strategy import load_names_strategy
from streamlit_utils.backend import build_response
from textcomplete import TextcompleteResult, textcomplete

# === Frontend ===
show_header()

if "txt" not in st.session_state:
    st.session_state["txt"] = ""

if "messages" not in st.session_state:
    st.session_state["messages"] = []


def on_change():
    print(st.session_state["txt"])


def on_select(textcomplete_result: TextcompleteResult):
    searchResult = textcomplete_result.get("searchResult", "")
    text = textcomplete_result.get("text", "")
    print(searchResult, text)
    st.session_state["txt"] = text

original_label: str = "Escribí tu pregunta o consulta MySQL."
txt: str = st.text_area(
    label=original_label,
    key="txt",
    on_change=on_change,
)
st.caption("Tipea @ para autocompletar")

textcomplete(
    area_label=original_label,
    strategies=[load_names_strategy()],
    on_select=on_select,
    max_count=5,
    stop_enter_propagation=True,
)

button = st.button("Enviar")

set_background()

if txt and button:
    # === Backend ===
    build_response(txt)