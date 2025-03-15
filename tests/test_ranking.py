from src.ranking.ranking_engine import StockRanker
from src.config.ranking_config import RANKING_CONFIG
from datetime import datetime, timedelta


# tests/test_ranking.py
def test_ranking_logic():
    test_articles = [
        {'sentiment': 1, 'publishedAt': datetime.now()},
        {'sentiment': 1, 'publishedAt': datetime.now()},
        {'sentiment': -1, 'publishedAt': datetime.now() - timedelta(hours=48)}
    ]
    
    ranker = StockRanker(RANKING_CONFIG)
    score = ranker.calculate_score(test_articles)
    assert 0.4 < score < 0.6  # Expected range