import numpy as np
from datetime import datetime

class StockRanker:
    def __init__(self, config):
        self.weights = config['weights']
        self.time_decay = config['time_decay']
        
    def calculate_score(self, articles):
        """Calculate ranking score for a stock"""
        if not articles:
            return 0.0  # Handle no-news case
            
        sentiments = [a['sentiment'] for a in articles]
        timestamps = [a['publishedAt'] for a in articles]
        
        # Sentiment component
        pos = sum(1 for s in sentiments if s == 1)
        neu = sum(1 for s in sentiments if s == 0)
        neg = sum(1 for s in sentiments if s == -1)
        sentiment_score = (2*pos + neu - neg) / len(sentiments)
        
        # Volume component (log scaling)
        volume = np.log(len(articles) + 1) / 3
        
        # Recency component (exponential decay)
        current_time = datetime.now()
        time_deltas = [(current_time - ts).total_seconds()/3600 for ts in timestamps]
        recency = np.mean([np.exp(-delta/self.time_decay['half_life_hours']) 
                         for delta in time_deltas])
        
        return (
            self.weights['sentiment'] * sentiment_score +
            self.weights['volume'] * volume +
            self.weights['recency'] * recency
        )