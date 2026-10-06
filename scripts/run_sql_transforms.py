import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST", "localhost")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME", "quick_commerce_db")

engine = create_engine(f"postgresql+psycopg2://postgres:{db_password}@{db_host}:5432/{db_name}")

sql_files = [
    "sql/transform_stockout_analysis.sql",
    "sql/transform_price_trends.sql",
]

with engine.begin() as conn:
    for file_path in sql_files:
        print(f"Running {file_path}...")
        with open(file_path, "r") as f:
            conn.execute(text(f.read()))
        print("  Done.")

print("All transformations applied successfully.")