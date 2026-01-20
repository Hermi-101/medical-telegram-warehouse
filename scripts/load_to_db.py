import os
import json
import pandas as pd
from sqlalchemy import create_engine, text  # Add 'text' here
from dotenv import load_dotenv

load_dotenv()

# Database connection
engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

def load_json_to_postgres():
    # Path to your data lake
    base_path = 'data/raw/telegram_messages'
    
    all_data = []

    # Iterate through date folders and files
    for date_folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, date_folder)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.json'):
                    with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        all_data.extend(data)

    if all_data:
        df = pd.DataFrame(all_data)
        
        with engine.connect() as conn:
            # 1. Create schema if not exists
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
            
            # 2. FORCE drop the table if it exists (the CASCADE part is key!)
            conn.execute(text("DROP TABLE IF EXISTS raw.telegram_messages CASCADE;"))
            conn.commit()
        
        # 3. Now load the data (since table is gone, 'replace' will work fine)
        df.to_sql('telegram_messages', engine, schema='raw', if_exists='replace', index=False)
        print(f"Successfully loaded {len(df)} rows into raw.telegram_messages")

if __name__ == "__main__":
    load_json_to_postgres()