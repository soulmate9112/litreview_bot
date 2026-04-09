import pydantic


class article_metadataSchema(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    doi: str
    title: str
    publication_year: int
    author_names: str
    abstract: str
