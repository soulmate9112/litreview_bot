from sqlalchemy.orm import Session
from sqlalchemy import select

from db.session import get_session
from orm.extracted_articlesORM import article_metadataORM
from schema.extracted_articlesSchema import (
    article_metadataSchema,
    multiple_article_metadataSchema,
)


from typing import List, Optional


class Article_metadata_repository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_entry(
        self, article_metadata_source: article_metadataSchema
    ) -> Optional[article_metadataSchema]:
        """Создает одну запись. Проверяет, нет ли уже записи с таким DOI."""

        # Проверяем, существует ли запись с таким DOI
        with self._session as session:
            existing = session.execute(
                select(article_metadataORM).where(
                    article_metadataORM.doi == article_metadata_source.doi
                )
            ).first()

            if existing:
                print(
                    f"Entry with DOI {article_metadata_source.doi} already exists. Skipping..."
                )
                return None

        # Создаем новую запись (исключаем id, если он есть)
        article_data = article_metadata_source.model_dump(exclude_none=True)
        article_metadata_orm = article_metadataORM(**article_data)

        with self._session as session:
            session.add(article_metadata_orm)
            session.commit()
            session.refresh(article_metadata_orm)

        return article_metadataSchema.model_validate(article_metadata_orm)

    def create_multiple_entries(
        self, article_metadata_list: multiple_article_metadataSchema
    ) -> multiple_article_metadataSchema:
        """Создает несколько записей. Пропускает те, у которых DOI уже существуют."""

        # Получаем все существующие DOI
        with self._session as session:
            existing_dois = set(
                session.execute(select(article_metadataORM.doi)).scalars().all()
            )
            existing_titles = set(
                session.execute(select(article_metadataORM.title)).scalars().all()
            )

        # Фильтруем новые статьи (проверка на дубликаты с БД)
        temp_articles = []
        for article in article_metadata_list.root:
            if (article.doi not in existing_dois) and (
                article.title not in existing_titles
            ):
                article_data = article.model_dump(exclude_none=True)
                temp_articles.append(article_metadataORM(**article_data))

        # Фильтруем дубликаты внутри самой пачки новых статей
        seen_dois = set()
        seen_titles = set()
        filtered_articles = []

        for orm_article in temp_articles:
            # Пропускаем, если DOI или title уже встречались в этой пачке
            if orm_article.doi in seen_dois or orm_article.title in seen_titles:
                print(
                    f"Skipping duplicate within batch: DOI={orm_article.doi}, Title={orm_article.title}"
                )
                continue

            # Добавляем в отфильтрованный список
            filtered_articles.append(orm_article)
            if orm_article.doi:
                seen_dois.add(orm_article.doi)
            if orm_article.title:
                seen_titles.add(orm_article.title)

        if not filtered_articles:
            print("No new articles to insert")
            return multiple_article_metadataSchema(root=[])

        # Сохраняем новые статьи
        with self._session as session:
            session.add_all(filtered_articles)
            session.commit()

            # Обновляем объекты, чтобы получить сгенерированные id
            for article in filtered_articles:
                session.refresh(article)

        # Конвертируем обратно в Pydantic
        created_schemas = [
            article_metadataSchema.model_validate(article)
            for article in filtered_articles
        ]

        return multiple_article_metadataSchema(root=created_schemas)

    def get_entry(self, id: int) -> Optional[article_metadataSchema]:
        """Получает одну запись по ID."""
        with self._session as session:
            article_metadata_orm = session.get(article_metadataORM, id)

            if article_metadata_orm is None:
                return None

            return article_metadataSchema.model_validate(article_metadata_orm)

    def get_multiple_entries(
        self, skip: int = 0, limit: int = 10
    ) -> List[article_metadataSchema]:
        """Получает несколько записей с пагинацией."""
        with self._session as session:
            query = select(article_metadataORM).offset(skip).limit(limit)
            results = session.execute(query).scalars().all()

            return [
                article_metadataSchema.model_validate(article) for article in results
            ]


def get_article_metadata_repository() -> Article_metadata_repository:
    return Article_metadata_repository(get_session())
