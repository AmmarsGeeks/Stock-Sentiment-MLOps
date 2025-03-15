import kagglehub
import pandas as pd
from src.pipeline.data_cleaner import NewsDataCleaner  # Assuming you have a data cleaner module

def run_news_pipeline():
    """
    Pipeline to fetch, clean, and process the Kaggle News Sentiment Analysis dataset.
    """
    try:
        # 1. Fetch data from Kaggle
        print("Fetching data from Kaggle...")
        df = kagglehub.load_dataset(
            "myrios/news-sentiment-analysis",
            file_path="News_Category_Dataset_v3.json",  # Replace with the actual file name
            adapter=kagglehub.KaggleDatasetAdapter.PANDAS
        )
        
        # 2. Clean data
        print("Cleaning data...")
        cleaned_data = NewsDataCleaner.clean_news_data(df)  # Replace with your cleaning logic
        
        # 3. Export data (optional)
        print("Exporting processed data...")
        cleaned_data.to_csv("processed_news.csv", index=False)
        
        # 4. Return cleaned data
        return cleaned_data
    
    except Exception as e:
        print(f"Error in pipeline: {str(e)}")
        return None


if __name__ == "__main__":
    # Run the pipeline
    data = run_news_pipeline()
    if data is not None:
        print("Pipeline completed successfully!")
        print("First 5 rows of cleaned data:")
        print(data.head())
    else:
        print("Pipeline failed.")