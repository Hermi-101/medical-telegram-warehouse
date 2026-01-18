from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from . import database, schemas

app = FastAPI(title="Kara Solutions: Medical Analytical API")

@app.get("/")
def home():
    return {"status": "API is online", "documentation": "/docs"}

# 1. Top Products (Already working, now with Schema)
@app.get("/api/reports/top-products", response_model=List[schemas.ProductResponse])
def get_top_products(limit: int = 10, db: Session = Depends(database.get_db)):
    query = text("SELECT message_text, views FROM staging.fct_messages ORDER BY views DESC LIMIT :limit")
    result = db.execute(query, {"limit": limit})
    return result.all()

# 2. Channel Activity (Trend of posts over time)
@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def get_channel_activity(channel_name: str, db: Session = Depends(database.get_db)):
    query = text("""
        SELECT message_date, count(*) as post_count 
        FROM staging.fct_messages m 
        JOIN staging.dim_channels c ON m.channel_key = c.channel_key 
        WHERE c.channel_name = :name 
        GROUP BY 1 ORDER BY 1
    """)
    result = db.execute(query, {"name": channel_name})
    return result.all()

# 3. Message Search (Keyword search)
@app.get("/api/search/messages", response_model=List[schemas.MessageSearchResponse])
def search_messages(query: str = Query(..., min_length=3), db: Session = Depends(database.get_db)):
    sql = text("SELECT message_text, views FROM staging.fct_messages WHERE message_text ILIKE :q LIMIT 20")
    result = db.execute(sql, {"q": f"%{query}%"})
    return result.all()

# 4. Visual Content Stats (YOLO Results)
@app.get("/api/reports/visual-content", response_model=List[schemas.VisualStat])
def get_visual_stats(db: Session = Depends(database.get_db)):
    # Note: Using the enriched table created in Task 3
    query = text("SELECT image_category, count(*) as count FROM staging.fct_image_detections GROUP BY 1")
    result = db.execute(query)
    return result.all()