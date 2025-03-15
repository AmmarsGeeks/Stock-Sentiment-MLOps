import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class ExportManager:
    @staticmethod
    def to_csv(rankings):
        df = pd.DataFrame(rankings, columns=['Company', 'Score'])
        df.to_csv('exports/ranking.csv', index=False)
        return 'exports/ranking.csv'
    
    @staticmethod
    def to_pdf(company, fig):
        doc = SimpleDocTemplate("exports/report.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        story.append(Paragraph(f"Analysis Report: {company}", styles['Title']))
        
        # Add plot image
        img_path = fig.to_image(format="png")
        story.append(Image(img_path, width=400, height=300))
        
        doc.build(story)
        return 'exports/report.pdf'