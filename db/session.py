import os
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FOLDER = os.path.join(BASE_DIR, "data")
EXPORT_FOLDER = os.path.join(BASE_DIR, "db_export_data")

os.makedirs(DB_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

DB_PATH_SAVED = os.path.join(DB_FOLDER, "article_metadata_saved.db")
DB_PATH_SENT = os.path.join(DB_FOLDER, "article_metadata_sent.db")
EXPORT_PATH = EXPORT_FOLDER  # Для использования в других функциях

db_URL_saved = f"sqlite:///{DB_PATH_SAVED}"
db_URL_sent = f"sqlite:///{DB_PATH_SENT}"

server_export_path = EXPORT_PATH

ENGINE_SENT: Engine = create_engine(db_URL_sent)
ENGINE_SAVED: Engine = create_engine(db_URL_saved)


def get_session_saved() -> Session:
    return Session(bind=ENGINE_SAVED)


def get_session_sent() -> Session:
    return Session(bind=ENGINE_SENT)
