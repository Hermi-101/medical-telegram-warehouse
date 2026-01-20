import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:5433/{os.getenv('DB_NAME')}")

df = pd.read_csv('data/enriched/yolo_detections.csv')
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS detection;"))
    conn.commit()

df.to_sql('yolo_results', engine, schema='detection', if_exists='replace', index=False)
print("Loaded YOLO results to database.")