import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = os.getenv("DB_NAME")

    connection_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_url)


def load_to_db(table_name: str, df: pd.DataFrame, chunksize: int = 50000,unique_col: str = "salesid"):
    """
    Efficiently loads a large DataFrame into PostgreSQL in chunks.
    """
    engine = get_engine()
    print(f"\nPreparing to load '{table_name}' into database...")
    print(f"Total rows: {len(df):,}")
    print(f"Data types before loading:\n{df.dtypes}\n")
    
    with engine.connect() as conn:
        existing_ids = pd.read_sql(f"SELECT {unique_col} FROM {table_name};", conn)[unique_col].to_list()
    print(f"Found {len(existing_ids):,} existing records in '{table_name}'.")
    
    df = df[~df[unique_col].isin(existing_ids)]
    print(f"Rows remaining: {len(df):,}")

    total_rows = len(df)
    for start in range(0, total_rows, chunksize):
        end = min(start + chunksize, total_rows)
        chunk = df.iloc[start:end]

        print(f"Loading rows {start:,} - {end:,} into '{table_name}'...")

        try:
            chunk.to_sql(
                name=table_name,
                con=engine,
                if_exists="append",
                index=False,
                method='multi',     # faster inserts
                chunksize=chunksize
            )
        except Exception as e:
            print(f"Error loading chunk: {e}")
            engine.dispose() # Dispose the engine to clear any pending transactions
            raise # Re-raise the exception after disposing the engine

    print(f"\n✅ Finished loading {table_name} ({total_rows:,} rows total)")
