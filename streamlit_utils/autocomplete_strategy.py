from textcomplete import StrategyProps
import json
import os

def load_names_strategy():
    # === Ruta relativa ===
    file_path = os.path.join(os.path.dirname(__file__), "data_autocomplete.json")

    # === Cargar JSON ===
    with open(file_path, "r", encoding="utf-8") as f:
        names_data = json.load(f)

    # === Crear estrategia ===
    return StrategyProps(
        id="names",
        match="\\B@(\\w*)$",
        template="(item) => item.name",
        replace="(item) => `${item.name}`",
        data=names_data,
        fuse_options={
            "keys": ["name"],
            "threshold": 0.3,
            "shouldSort": True
        }
    )