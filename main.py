# main.py
import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from transformers import pipeline

# Configuration
NEWS_API_KEY = '381793b3d6834758918838bca0cf52ee'
MODEL_NAME = "ProsusAI/finbert"
LABEL_MAPPING = {'positive': 1, 'neutral': 0, 'negative': -1}
RANKING_WEIGHTS = {
    'sentiment_strength': 0.5,
    'article_volume': 0.3,
    'recency': 0.2
}

# Initialize components
newsapi = NewsApiClient(api_key=NEWS_API_KEY)
sentiment_analyzer = pipeline("text-classification", model=MODEL_NAME)

class NewsFetcher:
    def get_articles(self, company_name):
        try:
            return newsapi.get_everything(
                q=company_name,
                language='en',
                sort_by='publishedAt',
                page_size=100
            )
        except Exception as e:
            print(f"News API Error: {str(e)}")
            return {'articles': []}
    
    def extract_headlines_with_dates(self, news_data):
        articles = []
        for article in news_data['articles']:
            try:
                published_at = datetime.fromisoformat(article['publishedAt'][:-1])
                articles.append({
                    'text': article['title'],
                    'published_at': published_at,
                    'source': article['source']['name'] if article['source'] else 'Unknown'
                })
            except:
                continue
        return articles

class SentimentAnalyzer:
    def analyze(self, headlines):
        if not headlines:
            return []
        try:
            results = sentiment_analyzer([h['text'] for h in headlines])
            return [
                {
                    'text': headline['text'],
                    'published_at': headline['published_at'],
                    'label': res['label'],
                    'score': res['score']
                }
                for headline, res in zip(headlines, results)
            ]
        except Exception as e:
            print(f"Sentiment Analysis Error: {str(e)}")
            return []

    def process_results(self, results):
        if not results:
            return pd.DataFrame()
        df = pd.DataFrame(results)
        df['sentiment'] = df['label'].map(LABEL_MAPPING)
        return df

def calculate_ranking_score(articles):
    """Calculate investment importance score using multiple factors"""
    if not articles:
        return 0.0, {'sentiment_strength': 0, 'article_volume': 0, 'recency': 0}
    
    current_time = datetime.now()
    
    # Sentiment strength component
    sentiment_scores = []
    for article in articles:
        score = article['score'] * article.get('sentiment', 0)
        sentiment_scores.append(score)
    sentiment_strength = np.mean(sentiment_scores) if sentiment_scores else 0
    
    # Article volume component (logarithmic scaling)
    article_volume = min(1, np.log(len(articles) + 1) / 3)
    
    # Recency component (exponential decay)
    time_deltas = [(current_time - art['published_at']).total_seconds() / 3600 for art in articles]
    recency_weights = [np.exp(-delta/24) for delta in time_deltas]
    recency = np.mean(recency_weights) if recency_weights else 0
    
    # Combine components
    final_score = (
        RANKING_WEIGHTS['sentiment_strength'] * sentiment_strength +
        RANKING_WEIGHTS['article_volume'] * article_volume +
        RANKING_WEIGHTS['recency'] * recency
    )
    
    # Return both score and components
    return final_score, {
        'sentiment_strength': sentiment_strength,
        'article_volume': article_volume,
        'recency': recency
    }

def analyze_multiple_stocks(companies):
    fetcher = NewsFetcher()
    analyzer = SentimentAnalyzer()
    results = []
    
    for company in companies:
        company = company.strip()
        if not company:
            continue
            
        try:
            # Fetch and process news
            raw_news = fetcher.get_articles(company)
            articles = fetcher.extract_headlines_with_dates(raw_news)
            analyzed_articles = analyzer.analyze(articles)
            df = analyzer.process_results(analyzed_articles)
            
            if df.empty:
                raise ValueError("No articles found")
                
            articles_list = df.to_dict('records')
            score, components = calculate_ranking_score(articles_list)
            results.append({
                'company': company,
                'score': max(0, min(1, score)),  # Ensure score is 0-1
                'components': components
            })
            
        except Exception as e:
            print(f"Error processing {company}: {str(e)}")
            results.append({
                'company': company,
                'score': 0.0,
                'components': {'sentiment_strength': 0, 'article_volume': 0, 'recency': 0}
            })
    
    return sorted(results, key=lambda x: x['score'], reverse=True)

def create_sentiment_chart(company, df):
    if df.empty:
        return go.Figure()
    
    positive = df[df['sentiment'] == 1]['sentiment']
    negative = df[df['sentiment'] == -1]['sentiment']

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=positive, name='Positive', marker_color='green'))
    fig.add_trace(go.Histogram(x=negative, name='Negative', marker_color='red'))
    
    fig.update_layout(
        title=f'Sentiment Distribution for {company}',
        xaxis_title='Sentiment',
        yaxis_title='Count',
        barmode='overlay',
        plot_bgcolor='white',
        showlegend=True
    )
    return fig

# Gradio Interface
with gr.Blocks(title="Stock Analysis System") as interface:
    gr.Markdown("# 📈 Stock Analysis System")
    
    with gr.Tab("🔍 Individual Analysis"):
        with gr.Row():
            with gr.Column():
                single_input = gr.Textbox(label="Enter Company Name", placeholder="e.g., Apple")
                single_btn = gr.Button("Analyze", variant="primary")
            with gr.Column():
                single_output = gr.Plot(label="Sentiment Distribution")
    
    with gr.Tab("🏆 Multi-Company Ranking"):
        with gr.Row():
            with gr.Column():
                multi_input = gr.Textbox(label="Enter Companies (comma-separated)", placeholder="e.g., Apple, Microsoft")
                rank_btn = gr.Button("Generate Ranking", variant="primary")
            with gr.Column():
                rank_list = gr.DataFrame(headers=["Rank", "Company", "Score"], label="Ranking")
                breakdown_chart = gr.Plot(label="Score Components Breakdown")
    
    # Individual Analysis Handler
    def handle_single_analysis(company):
        fetcher = NewsFetcher()
        analyzer = SentimentAnalyzer()
        
        raw_news = fetcher.get_articles(company)
        articles = fetcher.extract_headlines_with_dates(raw_news)
        analyzed_articles = analyzer.analyze(articles)
        df = analyzer.process_results(analyzed_articles)
        
        return create_sentiment_chart(company, df)
    
    single_btn.click(
        fn=handle_single_analysis,
        inputs=single_input,
        outputs=single_output
    )
    
    # Ranking Handler
    def handle_ranking(companies):
        ranked = analyze_multiple_stocks([c.strip() for c in companies.split(",") if c.strip()])
        
        # Prepare ranking list
        ranking_df = pd.DataFrame([
            [i+1, item['company'], f"{item['score']:.2f}"] 
            for i, item in enumerate(ranked)
        ], columns=["Rank", "Company", "Score"])
        
        # Prepare breakdown chart
        if ranked:
            components_df = pd.DataFrame({
                'Company': [item['company'] for item in ranked],
                'Sentiment': [item['components']['sentiment_strength'] for item in ranked],
                'Volume': [item['components']['article_volume'] for item in ranked],
                'Recency': [item['components']['recency'] for item in ranked]
            })
            
            fig = go.Figure()
            for col in ['Sentiment', 'Volume', 'Recency']:
                fig.add_trace(go.Bar(
                    x=components_df['Company'],
                    y=components_df[col],
                    name=col
                ))
            
            fig.update_layout(
                title="Score Components Breakdown",
                barmode='group',
                yaxis_title="Component Value",
                xaxis_title="Company"
            )
        else:
            fig = go.Figure()
        
        return ranking_df, fig
    
    rank_btn.click(
        fn=handle_ranking,
        inputs=multi_input,
        outputs=[rank_list, breakdown_chart]
    )

if __name__ == "__main__":
    interface.launch(share=True)