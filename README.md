# 🧠 Sentiment Analysis Platform

AI-powered multi-language sentiment analysis API built with **FastAPI**, **Transformers**, and **Redis**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

| Feature | Status |
|---------|--------|
| 🇬🇧 English Sentiment | ✅ DistilBERT |
| 🇸🇦 Arabic Sentiment | ✅ AraBERT v2 |
| 🇫🇷 French, 🇪🇸 Spanish, 🇩🇪 German | ✅ XLM-RoBERTa |
| 🇮🇳 Hindi, 🇷🇺 Russian, 🇨🇳 Chinese | ✅ XLM-RoBERTa |
| 📦 Batch Processing | ✅ Up to 100 texts |
| ⚡ Redis Caching | ✅ &lt; 1ms cached responses |
| 🔐 API Key Authentication | ✅ Multi-tier rate limits |
| 💾 Database Storage | ✅ SQLite / PostgreSQL |
| 📊 Prometheus Metrics | ✅ `/metrics` endpoint |
| 🧪 pytest Tests | ✅ 7+ tests |
| 🎨 Frontend Dashboard | ✅ HTML + JS |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Redis (optional, for caching)

### 1. Clone & Setup

```bash
git clone https://github.com/YOUR_USERNAME/sentiment-analysis-platform.git
cd sentiment-analysis-platform

python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

pip install -r requirements.txt