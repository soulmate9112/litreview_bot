from sqlalchemy.orm import Session
from sqlalchemy import select

from db.session import get_session_sent
from orm.ORMclasses import saved_articleORM, sent_articleORM
from schema.extracted_articlesSchema import (
    multiple_article_metadataSchema,
    article_metadataSchema,
)

from crud.saved_article_repository import (
    Saved_article_repository,
    get_saved_article_repository,
)

from db.session import ENGINE_SAVED, ENGINE_SENT
from typing import List, Sequence


class Sent_article_repository:
    def __init__(self, session: Session) -> None:
        self._session = session

    # Include the just sended articles
    def put_unsent_articles(
        self, sent_articles: Sequence[saved_articleORM]
    ) -> multiple_article_metadataSchema:
        with self._session as session:
            session.add_all(sent_articles)
            session.commit()

        pydantic_unsent_articles = [
            article_metadataSchema.model_validate(unsent_article)
            for unsent_article in unsent_articles
        ]

        return multiple_article_metadataSchema(root=pydantic_unsent_articles)

    def get_sent_articles(self) -> multiple_article_metadataSchema:
        with self._session as session:
            query = select(saved_articleORM)
            sent_articles = session.execute(query).scalars().all()
            session.commit()

        pydantic_sent_articles = [
            article_metadataSchema.model_validate(sent_articles)
            for sent_article in sent_articles
        ]

        return multiple_article_metadataSchema(root=pydantic_sent_articles)


def get_sent_article_repository() -> Sent_article_repository:
    return Sent_article_repository(get_session_sent())
