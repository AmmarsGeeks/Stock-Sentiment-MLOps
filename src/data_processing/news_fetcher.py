from newsapi import NewsApiClient
from src.config import constants as const

class NewsFetcher:
    def __init__(self):
        self.newsapi = NewsApiClient(api_key=const.NEWS_API_KEY)
    
    def get_articles(self, company_name):
        """Fetch raw news articles"""
        return self.newsapi.get_everything(
            q=company_name,
            language='en',
            sort_by='publishedAt',
            page_size=100  # Max allowed by API
        )
    
    @staticmethod
    def extract_headlines(news_data):
        """Extract headlines from raw news response"""
        return [article['title'] for article in news_data['articles']]