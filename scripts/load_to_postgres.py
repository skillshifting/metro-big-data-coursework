from pathlib import Path

import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from sqlalchemy.engine import URL
from inspect_data import DataSetScanner
import pandas as pd

from library import files


for file,config in files.items():
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir.parent / "data" / "raw" / file
    scanner = DataSetScanner(file_path)
    if file == "data-624-11-09-2026.csv":
        scanner.drop_sparse_columns()

    df = scanner.df.rename(columns=config["rename"])
    

    # print(scanner.df.head())

    # print(df.head())

    env_path = Path(__file__).resolve().parents[1]/".env"
    load_dotenv(env_path)

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host='localhost',
        port=5432,
        database=os.getenv("POSTGRES_DB")
    )

    engine = create_engine(url)

    df.to_sql(
        name = config["table"],
        con = engine,
        schema = 'staging',
        if_exists="append",
        index = False
    )
