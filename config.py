from dotenv import load_dotenv
import os

# === Funcion para el path de las variables de entorno  ===
def load_env():
    load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env')))