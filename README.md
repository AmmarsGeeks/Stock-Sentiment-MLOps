# Stock Sentiment Analysis & Ranking System 📈

A comprehensive MLOps solution for analyzing financial news sentiment and ranking stocks based on market impact.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-3.0-green)](https://gradio.app/)
[![Transformers](https://img.shields.io/badge/Transformers-4.30-red)](https://huggingface.co/docs/transformers/index)

---

## 🏗️ Infrastructure

### **Data Pipeline**
1. **Data Ingestion**: Curated financial news data from [Kaggle News Sentiment Dataset](https://www.kaggle.com/datasets/myrios/news-sentiment-analysis).
2. **Local Storage**: News articles stored in SQLite database with schema:
   - `articles(id, title, content, date, source)`
   - `sentiments(article_id, label, score)`
3. **Real-time Processing**:
   - Continuous model validation using incremental learning.
   - Automated data versioning with DVC.

### **MLOps Architecture**
```plaintext
Data Layer (SQLite) → Processing Layer → Model Serving → Application Layer (Gradio)
```

## 🤖 Sentiment Analysis

- **Technical Implementation**: 
 Base Model: FinBERT (Financial Domain BERT).

- **Custom Training**:

Fine-tuned on Kaggle dataset (10,000 labeled articles).

Dynamic threshold adjustment based on market volatility.

- **Processing Flow:**:


Text cleaning (stopwords, lemmatization).

Context-aware sentiment scoring.

Confidence-based filtering (score > 0.7).

## Visualization
Interactive Plotly histograms.

Real-time sentiment distribution updates.



## 🏆 Ranking System


### Algorithm Components
```bash

Ranking Score = 
  (Sentiment Strength × 0.5) + 
  (Article Volume × 0.3) + 
  (Recency Factor × 0.2)

```

## Key Metrics

Sentiment Strength: Weighted average of confidence scores.

Article Volume: log(n_articles) scaled 0-1.

Recency Factor: Exponential decay (24h half-life).

## 🚀 Getting Started


### Installation
```bash

git clone https://github.com/AmmarsGeeks/Stock-Sentiment-MLOps
cd stock-sentiment-mlops
pip install -r requirements.txt

```


### Configuration
```bash
# Copy the example environment file:
cp .env.example .env


```
Edit .env to include:

Database path.

Model parameters.

### Run Application

```bash
python main.py

```


### 📊 API Reference

#### GET /analyze

Fetch sentiment analysis for a specific company:

```bash
curl http://localhost:8000/analyze?company=Apple

```

#### POST /rank
Rank multiple companies based on news sentiment:


```bash
curl -X POST http://localhost:8000/rank \
  -H "Content-Type: application/json" \
  -d '{"companies": ["Apple", "Microsoft", "Google"]}'
```

#### 🛠️ Technologies Used
Rank multiple companies based on news sentiment:


```bash
Python: Core programming language.

Gradio: For building the web interface.

Transformers: For sentiment analysis using FinBERT.

SQLite: For local data storage.

Plotly: For interactive visualizations.

```

#### 🤝 Acknowledgments

Kaggle: For providing the News Sentiment Analysis Dataset.

Hugging Face: For the FinBERT model.

Gradio: For the easy-to-use web interface framework.

