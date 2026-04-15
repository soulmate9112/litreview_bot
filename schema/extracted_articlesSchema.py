import pydantic
from typing import List


class article_metadataSchema(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    doi: str | None = None
    title: str | None = None
    publication_year: int | None = None
    authors: str | None = None
    abstract: str | None = None


class multiple_article_metadataSchema(pydantic.RootModel):
    root: List[article_metadataSchema]
