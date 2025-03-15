from src.data_processing.news_fetcher import NewsFetcher

class NewsPreview:
    def __init__(self):
        self.fetcher = NewsFetcher()
    
    def get_top_headlines(self, company, n=5):
        news = self.fetcher.get_articles(company)
        return [{
            'headline': article['title'],
            'sentiment': SentimentAnalyzer.process_single_result(
                sentiment_analyzer(article['title'])),
            'date': article['publishedAt'][:10]
        } for article in news['articles'][:n]]