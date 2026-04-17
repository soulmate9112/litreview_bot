from pydantic import PositiveInt

from sqlalchemy import Integer, String, Column, create_engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeBase


class Base(DeclarativeBase):
    pass


class saved_articleORM(Base):
    __tablename__ = "saved_article"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    doi: Mapped[str] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(500), nullable=True)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=True)
    authors: Mapped[str] = mapped_column(String(1000), nullable=True)
    abstract: Mapped[str] = mapped_column(String(1000), nullable=True)


class sent_articleORM(Base):
    __tablename__ = "sent_article"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    doi: Mapped[str] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(500), nullable=True)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=True)
    authors: Mapped[str] = mapped_column(String(1000), nullable=True)
    abstract: Mapped[str] = mapped_column(String(1000), nullable=True)
