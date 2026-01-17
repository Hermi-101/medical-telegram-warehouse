# Medical Telegram Data Warehouse

An end-to-end ELT pipeline that extracts medical business data from Ethiopian Telegram channels, transforms it into a Star Schema using dbt, and enriches it with YOLOv8 object detection.

## 🏗 Architecture
**Telegram API** → **Data Lake (JSON/Images)** → **PostgreSQL (Raw)** → **dbt (Staging/Marts)** → **FastAPI**

## 🚀 Setup Instructions

### 1. Prerequisites
- Docker & Docker Desktop
- Python 3.10+
- Telegram API Credentials (api_id, api_hash)

### 2. Installation
```bash
git clone https://github.com/your-username/medical-telegram-warehouse.git
cd medical-telegram-warehouse
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
