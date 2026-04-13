import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import Session
from orm.extracted_articles import article_metadataORM
from db.session import get_session


def export_database(server_url, server_export_path):
    # if not os.path.exists(server_url):
    #     raise FileNotFoundError(f"Server database is not found at the following path:{server_url}")
    export_model(get_session(), article_metadataORM, server_export_path)


def export_model(session, model_class, server_export_path):
    table_name = model_class.__tablename__
    try:
        objects = session.query(model_class).all()
        if not objects:
            print("No data found for table {table_name}")
            return
        data = []
        for object in objects:
            row_data = {}
            for column in model_class.__table__.columns:
                value = getattr(object, column.name)
                if hasattr(value, "isoformat"):
                    value = value.isoformat()
                row_data[column.name] = value
            data.append(row_data)

        df = pd.DataFrame(data)
        csv_path = os.path.join(server_export_path, f"{table_name}.csv")
        df.to_csv(csv_path, index=False, header=True)
    except Exception as e:
        print(f"Error exporting {table_name}: {e}")
