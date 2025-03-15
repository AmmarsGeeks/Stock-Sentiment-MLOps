from transformers import pipeline
from src.config import constants as const
import pandas as pd


class SentimentAnalyzer:
    def __init__(self):
        self.model = pipeline("text-classification", model=const.MODEL_NAME)
    
    def analyze_headlines(self, headlines):
        return self.model(headlines)
    
    @staticmethod
    def process_results(results):
        """Process batch results and return DataFrame"""
        df = pd.DataFrame(results)
        df['sentiment'] = df['label'].map(const.LABEL_MAPPING)
        return df.drop(columns=['label'])
    
    @staticmethod
    def process_single_result(result):
        """Process individual result for ranking"""
        return const.LABEL_MAPPING[result['label']]