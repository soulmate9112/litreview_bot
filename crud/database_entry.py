from sqlalchemy.orm import Session
from sqlalchemy import select

from db.session import get_session
from orm.extracted_articles import article_metadataORM
from schema.extracted_articles import article_metadataSchema


class Article_metadata_repository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_entry(
        self, article_metadata_source: article_metadataSchema
    ) -> article_metadataSchema:
        article_metadata_orm = article_metadataORM(
            **article_metadata_source.model_dump()
        )  # pyright: ignore [reportCallIssue]
        with self._session as session:
            session.add(article_metadata_orm)
            session.commit()

        return article_metadataSchema.model_validate(article_metadata_orm)

    def get_entry(self, id: int) -> article_metadataSchema | None:
        with self._session as session:
            article_metadata_orm = session.get(article_metadataORM, id)

            if article_metadata_orm is None:
                return None
            if isinstance(article_metadata_orm, article_metadataORM):
                return article_metadataSchema.model_validate(article_metadata_orm)


def get_booking_repository() -> Article_metadata_repository:
    return Article_metadata_repository(get_session())
