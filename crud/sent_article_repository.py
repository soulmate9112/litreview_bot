from sqlalchemy.orm import Session
from sqlalchemy import select

from db.session import get_session
from orm.ORMclasses import saved_article_metadataORM
from schema.extracted_articlesSchema import (
    article_metadataSchema,
    multiple_article_metadataSchema,
)


from typing import List, Optional


class Sent_article_repository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_unsent_articles():
        pass
