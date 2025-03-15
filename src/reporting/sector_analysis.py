import yaml
from src.config import sectors

class SectorAnalyzer:
    def __init__(self):
        with open('src/config/sectors.yaml') as f:
            self.sector_map = yaml.safe_load(f)
        
    def get_sector_companies(self, sector):
        return [c for c, s in self.sector_map.items() if s == sector]
    
    def calculate_benchmarks(self, sector):
        companies = self.get_sector_companies(sector)
        scores = analyze_multiple_stocks(companies)
        return pd.DataFrame(scores, columns=['company', 'score'])