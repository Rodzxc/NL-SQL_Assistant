
import ast, re, json, os
from db.db_conn import db

# === Crear lista para el autocompletado ===
def query_as_list(db, query): 
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))

# --- Extraer los nombres ---
proveedores = query_as_list(db, "SELECT DISTINCT Nombre FROM proveedores")
productos = query_as_list(db, "SELECT DISTINCT Producto FROM productos")
almacenes = query_as_list(db, "SELECT DISTINCT Almacen FROM productos")

# --- Enlistarlos ---
names = list(proveedores + productos + almacenes)

# --- Armar estructura esperada por StrategyProps ---
data_json = [{"name": name_} for name_ in names]

# --- Guardar en archivo ---
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data_autocomplete.json")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data_json, f, ensure_ascii=False, indent=2)

print("✅ Archivo 'data_autocomplete.json' generado.")