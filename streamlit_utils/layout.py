import streamlit as st
from streamlit_utils.img_base64 import get_img_as_base64

# === Fondo ===
def set_background(path="./img/fondo.png"):
    img = get_img_as_base64(path)
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), 
            url("data:image/png;base64,{img}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}

    [data-testid="stHeader"] {{
    background-color: rgba(0 , 0 , 0 , 0);
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# === Header ===
def show_header():
    st.set_page_config(page_title="Asistente IA", page_icon="🤖")
    st.markdown("""
                    <h1 style='font-size: 2.5em; font-weight: 600;'>
                        <span style="font-family:Segoe UI Emoji, Apple Color Emoji, Noto Color Emoji, sans-serif;">🤖</span> Asistente Inteligente
                    </h1>
                """, unsafe_allow_html=True)