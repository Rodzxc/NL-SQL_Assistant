from langchain_core.prompts import ChatPromptTemplate
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from chain.llm import llm
from db.db_conn import db
from functools import lru_cache

# === Prompt para la Tool de SQL ===
system="""Eres un experto en {dialect}. Dada una pregunta de entrada, crea una consulta {dialect} sintácticamente correcta para ejecutar.

A menos que el usuario especifique en la pregunta, consulta como máximo {top_k} resultados. Puedes ordenar los resultados para devolver los datos más informativos de la base de datos.

Nunca consultes todas las columnas de una tabla. Debes consultar solo las columnas necesarias para responder la pregunta.

Presta atención a usar únicamente los nombres de columnas visibles en las tablas indicadas abajo. Ten cuidado de no consultar columnas que no existen. Además, presta atención a qué columna pertenece a qué tabla.

Utiliza solo las siguientes tablas:
{table_info}

Esquema de la tabla productos:
{schema_productos}

Esquema de la tabla Proveedores:
{schema_proveedores}

Escribe un primer borrador de la consulta. Luego, revisa cuidadosamente la consulta {dialect} para detectar errores comunes, incluyendo:

- Uso de NOT IN con valores NULL
- Uso de UNION cuando debió usarse UNION ALL
- Uso de BETWEEN para rangos exclusivos
- Incompatibilidad de tipos de datos en condiciones
- Uso correcto de comillas en identificadores
- Uso del número correcto de argumentos en funciones
- Conversión adecuada de tipos de datos (casting)
- Uso correcto de columnas en los JOINs
- Uso correcto de LIKE '%...%' cuando te pregunten por un producto,almacen o proveedor en particular

Ten en cuenta que:
              * Tienes 2 tablas (productos, Proveedores) y se conectan mediante `ProveedorID`.
              * Las columnas `Ingresos_ABC`, `Cantidad_ABC` , `Importancia_ABCD` indican la importancia. La última indica un nivel de importancia general.
              * Class A: todos los productos o proveedores más importantes. Puedes usar "... ORDER BY `columna` ASC ..." para obtener los más importantes.

Usa el siguiente formato:

Primer borrador: <<FIRST_DRAFT_QUERY>>
Respuesta final: <<FINAL_ANSWER_QUERY>>

"""
@lru_cache()
def build_prompt():
    # 1. Crear el toolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    # 2. Obtener herramientas individuales
    tools_sql = toolkit.get_tools()
    # 3. Filtrar las herramientas necesarias
    tool_dict = {tool.name: tool for tool in tools_sql}
    # 4. Ejecutar las herramientas anteriores para obtener la info
    table_info = tool_dict["sql_db_list_tables"].invoke({})
    schema_productos = tool_dict["sql_db_schema"].invoke('productos')
    schema_proveedores = tool_dict["sql_db_schema"].invoke('proveedores')

    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", "{input}")]
    ).partial(dialect=db.dialect, table_info=table_info, schema_productos=schema_productos, schema_proveedores=schema_proveedores)

    return prompt