from pydantic import PositiveInt

from sqlalchemy import Integer, String, Column, create_engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

engine = create_engine(
    "sqlite:///:memory:",
)

Base: type[DeclarativeMeta] = declarative_base()


class article_metadataORM(Base):
    __tablename__ = "article_metadata"

    doi: Mapped[str] = mapped_column(primary_key=True, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=True)
    author_names: Mapped[str] = mapped_column(String, nullable=True)
    abstract: Mapped[str] = mapped_column(String, nullable=True)
