# src/ranking/business_rules.py
class SectorAdjuster:
    def __init__(self, sector_weights):
        self.weights = sector_weights
        
    def apply_sector_adjustment(self, score, sector):
        return score * self.weights.get(sector, 1.0)