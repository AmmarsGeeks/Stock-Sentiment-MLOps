# data_manager.py
import sqlite3
from datetime import datetime

class HistoryManager:
    def __init__(self):
        self.conn = sqlite3.connect('data/processed/history.db')
        self._create_table()
    
    def _create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS analysis_history
                            (date TEXT, company TEXT, score REAL, 
                             positive INTEGER, negative INTEGER)''')
    
    def log_analysis(self, company, score, positives, negatives):
        self.conn.execute('''INSERT INTO analysis_history 
                           VALUES (?, ?, ?, ?, ?)''',
                          (datetime.now().isoformat(), company, 
                           score, positives, negatives))
        self.conn.commit()
    
    def get_history(self, company, days=30):
        return pd.read_sql('''SELECT * FROM analysis_history 
                            WHERE company = ? AND 
                            date >= datetime('now', '-? days') 
                            ORDER BY date''', 
                         self.conn, params=(company, days))