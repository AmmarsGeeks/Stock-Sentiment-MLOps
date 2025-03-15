# src/monitoring/performance.py
import mlflow

class PerformanceTracker:
    def log_ranking_run(self, companies):
        with mlflow.start_run():
            mlflow.log_param("companies", companies)
            mlflow.log_metric("num_companies", len(companies))