# Event-Based Living Backend

An intelligent event discovery and management system that crawls websites, extracts event information using AI, and provides a RESTful API for accessing structured event data.

## 🌟 Overview

This project is designed to automate the process of event discovery and management in Munich, Germany. It crawls event-related websites, uses AI to extract and classify event information, performs intelligent deduplication using vector embeddings, and stores the results in both relational and vector databases for efficient querying.

## 🏗️ Architecture

The system consists of two main components:

### 1. Event Service (`event_service/`)
- **Web Crawler**: Scrapes event websites to collect raw content
- **AI Classification**: Uses Google's Gemini AI to extract structured event data
- **Vector Embeddings**: Creates embeddings for intelligent deduplication
- **Database Storage**: Stores events in PostgreSQL with pgVector for similarity search

### 2. API Service (`api/`)
- **FastAPI REST API**: Provides endpoints to access processed event data
- **CORS Support**: Configured for cross-origin requests
- **Event Management**: List and retrieve individual events

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **AI/ML**: 
  - Google Gemini 2.5 Flash for event classification
  - LangChain for AI orchestration
  - HuggingFace embeddings (nomic-ai/nomic-embed-text-v1.5)
- **Database**: 
  - PostgreSQL with pgVector extension for vector similarity search
  - SQLAlchemy ORM
- **Web Scraping**: BeautifulSoup4, Requests
- **Additional Services**: 
  - Tavily API for event enrichment
  - Docker for containerization

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Virtual environment (venv or .venv)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd event-based-living
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 5. Start Database Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL with pgVector (port 5432)
- Adminer database admin interface (port 8080)

### 6. Run the Event Service

```bash
python -m event_service
```

### 7. Start the API Server

```bash
./start_backend.sh
```

The API will be available at `http://localhost:8000`

## 📊 Database

### PostgreSQL Configuration
- **Host**: localhost:5432
- **Database**: postgres
- **User**: app
- **Password**: password

### Database Access
- **Adminer UI**: http://localhost:8080
- **Connection String**: `postgresql+psycopg://app:password@localhost:5432/postgres`

## 🔄 Event Processing Pipeline

1. **Crawling**: The system reads URLs from `event_service/sites.txt` and crawls them for content
2. **Classification**: Raw HTML content is processed by Gemini AI to extract structured event data
3. **Deduplication**: Events are deduplicated using vector similarity to avoid duplicates
4. **Enrichment**: Missing event details are enriched using Tavily search (TODO: implementation pending)
5. **Storage**: Events are stored in both relational and vector databases

## 🎯 Supported Event Types

- Concerts
- Festivals  
- General Events
- Club Events
- Parties
- Restaurant Events
- Bar Events
- Other

## 🌐 API Endpoints

### Get All Events
```http
GET /events
```
Returns up to 50 recent events.

### Get Single Event
```http
GET /events/{event_id}
```
Returns details for a specific event by ID.

## 📁 Project Structure

```
event-based-living/
├── api/                    # FastAPI application
│   ├── __init__.py
│   └── api.py             # API endpoints
├── event_service/         # Core event processing
│   ├── __init__.py
│   ├── __main__.py        # Service entry point
│   ├── main.py           # Main processing logic
│   ├── models.py         # Pydantic data models
│   ├── repository.py     # Database models and connection
│   ├── crawler.py        # Web scraping functionality
│   ├── classification_utils.py  # AI classification
│   ├── deduplication_utils.py   # Vector-based deduplication
│   ├── embedding_utils.py       # Embedding utilities
│   ├── enrichment_utils.py      # Event enrichment (TODO)
│   ├── db_utils.py             # Database utilities
│   ├── sites.txt              # URLs to crawl
│   ├── skip.txt               # URLs to skip
│   ├── enums/                 # Enumerations
│   │   ├── event_types.py     # Event type definitions
│   │   └── models.py          # AI model configurations
│   └── results/              # Crawled content storage
├── tests/                    # Unit tests
├── docker-compose.yml       # Database services
├── requirements.txt         # Python dependencies
├── start_backend.sh        # API startup script
└── README.md              # This file
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 🔧 Configuration

### Crawler Configuration
- Edit `event_service/sites.txt` to add/remove websites to crawl
- Modify `event_service/skip.txt` to exclude specific URL patterns

### AI Model Configuration
- Rate limiting: 15 requests per minute for Gemini API
- Embedding model: nomic-ai/nomic-embed-text-v1.5 (trust_remote_code=True)

### Database Configuration
- Vector similarity threshold: 0.05 (configurable in deduplication)
- Collection name: "events"

## 🚀 Deployment

The application is containerized and can be deployed using Docker:

1. Build and start all services:
```bash
docker-compose up --build
```

2. The API will be available on the configured port with persistent data storage.

## 📞 Support

For questions or issues, please open a GitHub issue or contact the development team.