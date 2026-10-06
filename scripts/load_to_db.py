import os
import json
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST", "localhost")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME", "quick_commerce_db")
data_path = os.getenv("DATA_PATH", "data/normalized_combined.json")

with open(data_path) as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(f"Raw records: {len(df)}")

df = df.drop_duplicates(subset=["name", "size", "pincode", "searched_category", "platform"])
print(f"After removing duplicates: {len(df)}")

engine = create_engine(f"postgresql+psycopg2://postgres:{db_password}@{db_host}:5432/{db_name}")
df.to_sql("stg_quick_commerce_prices", engine, if_exists="replace", index=False)
print("Loaded into stg_quick_commerce_prices successfully.")