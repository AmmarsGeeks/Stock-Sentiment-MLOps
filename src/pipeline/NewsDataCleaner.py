import pandas as pd

class NewsDataCleaner:
    @staticmethod
    def clean_news_data(df):
        """
        Clean and preprocess the news dataset.
        """
        # 1. Drop duplicates
        df = df.drop_duplicates(subset=['title', 'content'])
        
        # 2. Handle missing values
        df = df.dropna(subset=['title', 'content'])
        
        # 3. Standardize text
        df['title'] = df['title'].str.lower().str.strip()
        df['content'] = df['content'].str.lower().str.strip()
        
        # 4. Convert sentiment labels to numerical values
        sentiment_mapping = {'positive': 1, 'neutral': 0, 'negative': -1}
        df['sentiment'] = df['sentiment'].map(sentiment_mapping)
        
        # 5. Filter out invalid sentiment values
        df = df[df['sentiment'].isin([-1, 0, 1])]
        
        return df