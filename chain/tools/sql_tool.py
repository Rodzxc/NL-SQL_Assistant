from langchain.chains import create_sql_query_chain
from .sql_tool_prompt import build_prompt
from chain.llm import llm
from db.db_conn import db
from sqlalchemy import text
from langchain_core.tools import tool

# === Confeccion de Tool SQL ===
# --- Parsear respuesta ---
def parse_final_answer(output: str) -> str:
    return output.split("Respuesta final: ")[1].strip("<<").strip(">>").strip("\n```")
    
# --- sql_tool ---
@tool
def sql_tool(user_question: str):
    """Ejecuta una consulta SQL de los productos y proveedores."""
    prompt = build_prompt()
    chain = create_sql_query_chain(llm, db, prompt=prompt) | parse_final_answer
    query = chain.invoke({"question": user_question})
    
    # Conexion a la base de datos y query SQL
    with db._engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        columns = list(result.keys())

        # Convertir filas a listas de valores serializables
        data_rows = []
        for row in rows:
            row_data = []
            for value in row:
                # Convertir tipos no serializables a string si es necesario
                if value is None:
                    row_data.append(None)
                elif isinstance(value, (str, int, float, bool)):
                    row_data.append(value)
                else:
                    row_data.append(str(value))
            data_rows.append(row_data)
    
    return {
        "query": query,
        "columns": columns,
        "rows": data_rows
    }

