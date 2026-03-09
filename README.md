# TravelGenie – AI Powered Trip Planning System

An intelligent, full-stack travel planning platform that generates optimized trip itineraries using LLMs, budget allocation algorithms, and real-time data integration.

## 🌟 Key Features

- **AI-Powered Itinerary Generation** – Google Gemini API for personalized travel recommendations
- **Smart Budget Allocation** – Intelligently distributes budgets across stays, food, transport, and activities
- **Algorithmic Optimization** – 0/1 Knapsack algorithm to select the most valuable activities within budget
- **Redis Caching** – Reduces API calls and improves response times
- **Interactive Frontend** – React + TypeScript with OpenStreetMap + Leaflet integration
- **Robust System Design** – Error handling, validation, and fallback mechanisms

## 🛠️ Tech Stack

**Backend:** FastAPI, Python, Google Gemini LLM API, Redis  
**Frontend:** React, TypeScript, OpenStreetMap, Leaflet  

## 🚀 Quick Start

### Option 1: Docker (Recommended) 🐳
```bash
docker-compose up
```

API runs on `http://localhost:8000` | Frontend on `http://localhost:5173`

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for details.

### Option 2: Manual Setup
**Backend**
```bash
cd travelgenie
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
```

**Frontend** (new terminal)
```bash
cd travelgenie-frontend
npm install
npm run dev
```

## 📊 Core Features

**Budget Allocation Engine** – Splits budgets intelligently based on travel cost patterns  
**Activity Selection** – Knapsack-based optimization to maximize experience within budget  
**Smart Caching** – Stores generated activities to reduce redundant LLM calls  
**Natural Input Parsing** – Supports inputs like "50K" and "1L" for budget entry  

## 🧪 Testing

```bash
pytest tests/ -v
pytest tests/ --cov=app
```

## 📝 License

MIT License

---
