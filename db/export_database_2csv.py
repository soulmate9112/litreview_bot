import pandas as pd
import sqlalchemy as sa
import os
from sqlalchemy.orm import Session
from orm.extracted_articlesORM import article_metadataORM
from schema.extracted_articlesSchema import (
    multiple_article_metadataSchema,
)
from db.session import ENGINE


def export_database(export_path: str):
    with Session(bind=ENGINE) as session:
        export_all_entries(session, article_metadataORM, export_path)


def export_all_entries(
    session: Session,
    model_class: type[article_metadataORM],
    export_path: str,
):
    table_name = model_class.__tablename__

    try:
        # Query all entries from the database table
        all_entries = session.query(model_class).all()

        if not all_entries:
            print(f"No entries found in table {table_name}.")
            return

        # Convert ORM objects to dictionaries
        data_to_export = []
        for entry in all_entries:
            row_dict = {c.name: getattr(entry, c.name) for c in entry.__table__.columns}
            data_to_export.append(row_dict)

        # Ensure directory exists
        os.makedirs(export_path, exist_ok=True)

        csv_path = os.path.join(export_path, f"{table_name}_all_entries.csv")
        pd.DataFrame(data_to_export).to_csv(csv_path, index=False, header=True)

        print(f"Exported {len(data_to_export)} entries to {csv_path}")

    except Exception as e:
        print(f"Error exporting {table_name}: {e}")
