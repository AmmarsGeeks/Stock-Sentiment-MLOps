import pandas as pd
from datetime import datetime
from src.data_processing.news_fetcher import NewsFetcher
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.utils.visualization import create_sentiment_chart
from src.ranking.ranking_engine import StockRanker
from src.config.ranking_config import RANKING_CONFIG

def fetch_news(company_name):
    """Wrapper function for news fetching"""
    fetcher = NewsFetcher()
    raw_news = fetcher.get_articles(company_name)
    return {
        'articles': raw_news['articles'],
        'headlines': fetcher.extract_headlines(raw_news)
    }

def analyze_multiple_stocks(companies):
    ranker = StockRanker(RANKING_CONFIG)
    scores = {}
    
    for company in companies:
        try:
            # Fetch and process news
            news_data = fetch_news(company)
            
            # Analyze sentiment
            analyzer = SentimentAnalyzer()
            sentiment_results = analyzer.analyze_headlines(news_data['headlines'])
            
            # Prepare articles data for ranking
            processed_articles = []
            for article, sentiment in zip(news_data['articles'], sentiment_results):
                processed_articles.append({
                    'sentiment': analyzer.process_single_result(sentiment),
                    'publishedAt': datetime.fromisoformat(article['publishedAt'][:-1])
                })
            
            scores[company] = ranker.calculate_score(processed_articles)
        except Exception as e:
            print(f"Error processing {company}: {str(e)}")
            scores[company] = 0.0
        
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def analyze_news_sentiment(company_name):
    # Existing implementation remains the same
    fetcher = NewsFetcher()
    news_data = fetcher.get_articles(company_name)
    headlines = fetcher.extract_headlines(news_data)
    
    analyzer = SentimentAnalyzer()
    results = analyzer.analyze_headlines(headlines)
    processed_df = analyzer.process_results(results)
    
    return create_sentiment_chart(processed_df, company_name)