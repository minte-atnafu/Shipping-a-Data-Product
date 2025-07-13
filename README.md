# 📊 Telegram Medical Business Analytics Platform

A production-grade, scalable data pipeline and analytics API that extracts, processes, and analyzes data from public Ethiopian medical business Telegram channels. This platform includes object detection for image content, a data warehouse for structured storage, and a FastAPI interface for analytical access.

---

## 🚀 Project Overview

**Goal:** Build an end-to-end data pipeline that:

* Scrapes medical-related messages and images from Telegram
* Stores and processes raw data in a structured and queryable format
* Detects visual content (e.g. product packaging) using YOLOv8
* Provides RESTful API access to cleaned and enriched data
* Is containerized, automated, and production-ready

---

## 🧰 Tools and Technologies

| Component          | Tool / Library          | Purpose                                    |
| ------------------ | ----------------------- | ------------------------------------------ |
| Scraping           | Telethon / Pyrogram     | Extract Telegram data                      |
| Object Detection   | YOLOv8 (ultralytics)    | Analyze images                             |
| Data Storage       | PostgreSQL              | Central data warehouse                     |
| Data Modeling      | dbt                     | Data transformations, tests, documentation |
| API Layer          | FastAPI, Uvicorn        | Serve data via REST API                    |
| Containerization   | Docker, Docker Compose  | Environment & deployment                   |
| Secrets Management | python-dotenv           | Load environment variables                 |
| Orchestration      | Dagster                 | Run, monitor, and schedule pipelines       |
| Logging            | Python `logging` module | Monitoring and debugging                   |

---

## 📦 Project Structure

```
my_project/
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── data/
│   └── raw/
│       ├── telegram_messages/YYYY-MM-DD/
│       └── images/channel_name/
├── scraper/
│   └── scrape.py
├── ingestion/
│   └── load_to_postgres.py
├── enrichment/
│   └── yolo_detection.py
├── dbt_project/
│   ├── models/
│   └── dbt_project.yml
├── api/
│   ├── main.py
│   ├── crud.py
│   ├── models.py
│   └── schemas.py
└── orchestrator/
    └── dagster_pipeline.py
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/telegram-medical-pipeline.git
cd telegram-medical-pipeline
```

### 2. Add Environment Variables

Create a `.env` file:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_NAME=telegram_db
DB_HOST=db
```

### 3. Build Docker Environment

```bash
docker-compose up --build
```

### 4. Run Dagster UI

```bash
dagster dev
```

---

## 📘 API Endpoints (Examples)

| Endpoint                                 | Description             |
| ---------------------------------------- | ----------------------- |
| `/api/reports/top-products?limit=10`     | Most mentioned products |
| `/api/channels/{channel}/activity`       | Activity by channel     |
| `/api/search/messages?query=paracetamol` | Keyword search          |

---

## 📈 Data Pipeline

1. **Extract**: Scrape Telegram data (messages, images)
2. **Load**: Store raw data in a data lake (JSON, images)
3. **Transform**: Use `dbt` to model clean and structured tables
4. **Enrich**: Run YOLOv8 for object detection in images
5. **Expose**: Serve data via FastAPI
6. **Orchestrate**: Schedule & monitor via Dagster

---

## ✅ Milestones

### Task 0 - Project Setup

* ✅ Initialized Git repository
* ✅ Created Dockerfile, docker-compose.yml
* ✅ Created requirements.txt
* ✅ Added .env and .gitignore
* ✅ Set up python-dotenv

### Task 1 - Scraping & Data Lake

* ✅ Scraped messages from multiple Telegram channels
* ✅ Collected and stored images
* ✅ Structured raw data in date-partitioned directories
* ✅ Implemented logging for error tracking

### Task 2 - Data Transformation (dbt)

* ✅ Loaded raw JSON into PostgreSQL
* ✅ Created dbt models: staging and marts (dim, fct)
* ✅ Ran tests: not\_null, unique
* ✅ Generated documentation via dbt

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Mintesinot Atnafu
[GitHub](https://github.com/minte-atnafu)

---

## 📬 Contact

Feel free to open issues or submit pull requests!
