from sqlalchemy.orm import Session
from sqlalchemy import select

from db.session import get_session
from orm.ORMclasses import saved_articleORM, sent_articleORM
from schema.extracted_articlesSchema import (
    article_metadataSchema,
    multiple_article_metadataSchema,
)
from db.session import ENGINE


from typing import List, Optional


class Sent_article_repository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_unsent_articles():
        with Session(bind=ENGINE) as session:
            dois_unsent = {doi for doi in (session.query(sent_articleORM.doi))}

        select_unsent = select(saved_articleORM).where(
            saved_articleORM.doi.not_in(list(dois_unsent))
        )
        unsent_articles = session.execute(select_unsent).scalars().all()
