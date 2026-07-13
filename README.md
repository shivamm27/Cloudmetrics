# 📊 CloudMetrics - Health Analytics Platform with AI Insights

A full-stack data analytics platform combining SQL database queries, AI-powered insights via Claude, and interactive Streamlit dashboards to analyze public health data across Indian states.

## 🎯 Overview

CloudMetrics is a production-ready analytics platform that demonstrates end-to-end data engineering. It covers all four critical gaps for fresher data analyst/scientist roles:

✅ **SQL** — Complex queries with CASE statements and aggregates  
✅ **BI Tools** — Interactive Streamlit dashboard with Plotly charts  
✅ **Cloud Deployment** — Live on Streamlit Cloud  
✅ **Generative AI** — Anthropic Claude API integration  

---

## ✨ Features

### 📍 Dashboard
- National health overview (total cases, deaths, recovery rate)
- Top 10 states by case count with interactive bar charts
- Mortality and recovery rate visualizations
- Real-time metrics display

### 📈 Analysis
- **Compare States** — Side-by-side metrics for multiple states
- **Mortality Analysis** — Scatter plot showing mortality vs case volume
- **Risk Assessment** — Categorizes states as Critical/High/Moderate
- **Recovery Trends** — Recovery rates across states

### 🤖 AI Insights (Claude API)
- **National Overview** — Claude analyzes data and generates health recommendations
- **State Performance** — AI identifies patterns in state-wise data
- **Mortality Deep Dive** — Expert analysis of mortality rates
- **Custom Queries** — Ask Claude questions about health data

### ⚙️ Settings
- API configuration guide
- Database information
- Project details

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Database** | SQLite3 |
| **Backend** | Python 3.9+ |
| **Data Processing** | Pandas |
| **Visualization** | Plotly |
| **Frontend** | Streamlit |
| **AI/LLM** | Anthropic Claude API |
| **Deployment** | Streamlit Cloud |

---

## 📂 Project Structure

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Claude API key from https://console.anthropic.com

### Installation

```bash
# 1. Clone repository
git clone https://github.com/YOUR-USERNAME/cloudmetrics.git
cd cloudmetrics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create database
python load_data.py

# 4. Set API key (Linux/Mac)
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# 4. Set API key (Windows PowerShell)
$env:ANTHROPIC_API_KEY='sk-ant-your-key-here'

# 5. Run app
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## 📊 SQL Queries

### 1. Top States by Cases
Retrieves top 10 states ranked by total cases

### 2. Mortality Rate
Calculates mortality percentage: (Deaths / Cases) × 100

### 3. Recovery Rate
Calculates recovery percentage: (Recovered / Cases) × 100

### 4. National Summary
Aggregates total cases, deaths, recovered, and overall mortality rate using SUM and COUNT functions

### 5. Risk Assessment
Uses CASE statement to categorize states:
- Critical: Cases > 100K AND Mortality > 2%
- High: Cases > 50K AND Mortality > 1.5%
- Moderate: All others

### 6. State Comparison
Parameterized queries for comparing selected states (prevents SQL injection)

---

## 🤖 Claude AI Integration

CloudMetrics uses Anthropic's Claude API to provide intelligent health analysis:

- Conversation history management for context
- Multiple insight types (national, state-level, mortality, custom)
- Professional health recommendations
- Natural language explanation of data patterns

---

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app" and select your repository
4. In Advanced settings, add secret: `ANTHROPIC_API_KEY = "sk-ant-your-key"`
5. Deploy and get live URL

---

## 🎓 What This Demonstrates

**SQL Skills:**
- Schema design with normalization
- Complex queries (CAST, ROUND, CASE statements)
- Aggregate functions (SUM, COUNT)
- Parameterized queries for security

**Data Engineering:**
- Database creation and management
- Data loading and transformation
- Error handling

**Generative AI:**
- Claude API integration
- Prompt engineering
- Conversation management

**Full-Stack Development:**
- Backend: Python with OOP
- Frontend: Streamlit dashboard
- Database: SQLite
- Visualization: Plotly
- Deployment: Cloud hosting

---

## 📝 Resume Bullet

---

## 🔐 Security

- API keys in `.gitignore` (never committed)
- Environment variables for sensitive data
- Parameterized SQL queries (injection-safe)
- Error handling without exposing sensitive info

---

## 📚 Resources

- Streamlit Docs: https://docs.streamlit.io
- Claude API: https://docs.anthropic.com
- SQLite: https://sqlite.org/docs.html
- Plotly: https://plotly.com/python/

---

## 📄 License

Open source - feel free to use and modify

---

Made with Python | SQLite | Streamlit | Claude API | Plotly | Pandas