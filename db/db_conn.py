from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from config import load_env
import os

# === Crear engine y db para conectarse con la cadena ===
load_env()
password_mysql = os.environ['PASSWORD_MYSQL']
database = os.environ['DATABASE']

env_ = os.environ.get('ENV', 'development')

# docker-compose
if env_ == 'production': # ENV = 'production'
    uri = f'mysql+pymysql://root:{password_mysql}@host.docker.internal:3306/{database}'
# Local
else:
    uri = f'mysql+pymysql://root:{password_mysql}@localhost/{database}'

engine = create_engine(uri)
db = SQLDatabase(engine=engine)