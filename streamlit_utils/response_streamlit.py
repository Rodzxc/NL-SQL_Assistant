import streamlit as st
from pandas import DataFrame
import json

# === Confecion de respuestas ===

# --- Respuesta del Grafo ---
def sql_query_response(user_input):
    try: 
        conn = st.connection('productosdb', type='sql')
        try:
            if not user_input.strip().lower().startswith("select"):
                return st.error("Solo se permiten consultas SELECT.")
            else:
                p_ = conn.query(user_input)
                st.dataframe(p_)
        except Exception as e:
            return st.error(f"Error en la consulta sql: {e}")
    
    except Exception as e:
            return st.error(f"Error en la conexion: {e}")

# --- Respuesta SQL directa de streamlit ---
def chain_response(rsp):
        try:
            if rsp.type.title() == "Ai":
                st.markdown(f"""
                                <p style="font-size: 1.0em;">
                                    <span style="font-family:Segoe UI Emoji, Apple Color Emoji, Noto Color Emoji, sans-serif;">🤖</span>
                                    <strong>Respuesta:</strong> {rsp.content}
                                </p>
                            """, unsafe_allow_html=True)
            
            elif rsp.type.title() == "Tool":
                try:
                    data = json.loads(rsp.content) 
                    query_sql = data['query']
                    cols = data['columns']
                    rows = data['rows']

                    df = DataFrame(columns=cols, data=rows)

                    st.markdown(f"**Consulta generada:**\n```sql\n{query_sql}\n```")
                    st.dataframe(df)
                
                except Exception as e:
                    st.markdown(f"Error en el procesamiento de la base de datos: {e}")

        except Exception as e:
            st.markdown(f"Error en 'Ai' o 'Tool': {e}")
            st.markdown(rsp.content)