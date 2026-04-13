from sqlalchemy import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import os

DB_PATH = "/db/data"  # Fixed location in container
EXPORT_PATH = "/db/db_export_data"  # Fixed location in container

server_URL = f"sqlite:///{DB_PATH}"
server_export_path = EXPORT_PATH

ENGINE: Engine = create_engine(server_URL)

os.makedirs(
    "C:/Users/Simon/MAIN_WORK_FOLDER/coding/litreview_telegram_bot/litreview_bot/db/data",
    exist_ok=True,
)
os.makedirs(
    "C:/Users/Simon/MAIN_WORK_FOLDER/coding/litreview_telegram_bot/litreview_bot/db_export",
    exist_ok=True,
)


def get_session() -> Session:
    with Session(bind=ENGINE) as session:
        return session
