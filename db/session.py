import os
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FOLDER = os.path.join(BASE_DIR, "db/data")
EXPORT_FOLDER = os.path.join(BASE_DIR, "db/db_export_data")

os.makedirs(DB_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_FOLDER, "article_metadata.db")
EXPORT_PATH = EXPORT_FOLDER  # Для использования в других функциях

server_URL = f"sqlite:///{DB_PATH}"
server_export_path = EXPORT_PATH

ENGINE: Engine = create_engine(server_URL)


def get_session() -> Session:
    return Session(bind=ENGINE)
