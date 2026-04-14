import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import os
from sqlalchemy import select
from sqlalchemy.orm import Session
from orm.extracted_articlesORM import article_metadataORM
from schema.extracted_articlesSchema import (
    multiple_article_metadataSchema,
    article_metadataSchema,
)
from db.session import get_session, EXPORT_FOLDER


def export_database(
    url, export_path: str, new_entries: multiple_article_metadataSchema
):
    # if not os.path.exists(server_url):
    #     raise FileNotFoundError(f"Server database is not found at the following path:{server_url}")
    ENGINE = create_engine(url)
    with Session(bind=ENGINE) as session:
        export_new_entries(session, article_metadataORM, new_entries, export_path)


def export_new_entries(
    session: Session,
    model_class: type[article_metadataORM],
    source_data: multiple_article_metadataSchema,
    export_path,
):
    table_name = model_class.__tablename__
    try:
        existing_dois = session.execute(select(model_class.doi)).scalars().all()
        existing_dois = set(existing_dois)

        data_to_export = []
        for item in source_data.root:
            if item.doi not in existing_dois:
                # Convert the Pydantic model to a dictionary
                row_dict = item.model_dump()

                # Handle ISO formatting for dates if any fields were datetime objects
                for key, value in row_dict.items():
                    if hasattr(value, "isoformat"):
                        row_dict[key] = value.isoformat()

                data_to_export.append(row_dict)

        if not data_to_export:
            print(
                f"No new data to export for table {table_name}. All entries already exist in DB."
            )
            return

        df = pd.DataFrame(data_to_export)

        # Ensure directory exists
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        csv_path = os.path.join(export_path, f"{table_name}_absent_in_db.csv")
        df.to_csv(csv_path, index=False, header=True)

        print(f"Exported {len(data_to_export)} new entries to {csv_path}")

    except Exception as e:
        print(f"Error exporting {table_name}: {e}")
