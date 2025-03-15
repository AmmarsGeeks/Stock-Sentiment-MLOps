# main.py
import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from src import (
    analyze_news_sentiment,
    analyze_multiple_stocks,
    export_results,
    get_historical_data,
    get_sector_benchmarks
)

# -------------------------
# New Core Functionality
# -------------------------

def create_historical_comparison(company):
    history = get_historical_data(company)
    if history.empty:
        return "No historical data available"
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=history['date'],
        y=history['score'],
        name='Score Trend',
        line=dict(color='#3498db', width=2)
    ))
    fig.update_layout(
        title=f"Historical Performance: {company}",
        xaxis_title="Date",
        yaxis_title="Score",
        template="plotly_white"
    )
    return fig

def generate_sector_report(sector):
    benchmarks = get_sector_benchmarks(sector)
    return {
        "top_companies": benchmarks.nlargest(5, 'score'),
        "sector_average": benchmarks['score'].mean(),
        "performance_chart": create_sector_chart(benchmarks)
    }

# -------------------------
# Enhanced UI Components
# -------------------------

with gr.Blocks(theme=gr.themes.Soft(), css=".gradio-container {max-width: 1200px !important}") as interface:
    gr.Markdown("# 📈 Advanced Stock Analysis Dashboard")
    
    # --------------- Single Company Tab ---------------
    with gr.Tab("🔍 Single Company Analysis"):
        with gr.Row():
            with gr.Column(scale=2):
                single_input = gr.Textbox(label="Company Name", placeholder="Enter a company name...")
                with gr.Row():
                    single_btn = gr.Button("Analyze", variant="primary")
                    pdf_btn = gr.Button("📥 Export PDF")
            with gr.Column(scale=3):
                single_output = gr.Plot(label="Sentiment Distribution")
                history_output = gr.Plot(label="Historical Trend")
        
        with gr.Accordion("📰 Recent News Headlines", open=False):
            news_preview = gr.DataFrame(label="Top Headlines", headers=["Headline", "Sentiment", "Date"])
    
    # -------------- Multi-Company Tab --------------
    with gr.Tab("🏆 Comparative Analysis"):
        with gr.Row():
            with gr.Column(scale=2):
                multi_input = gr.Textbox(label="Company List", placeholder="Example: Apple, Google, Microsoft")
                sector_dropdown = gr.Dropdown(
                    label="Sector Benchmark",
                    choices=["Technology", "Energy", "Finance", "Healthcare"],
                    value="Technology"
                )
                with gr.Row():
                    rank_btn = gr.Button("Generate Ranking", variant="primary")
                    csv_btn = gr.Button("📥 Export CSV")
            with gr.Column(scale=3):
                rank_list = gr.HTML(label="Ranking Summary")
                rank_output = gr.Plot(label="Interactive Comparison")
        
        with gr.Row():
            sector_chart = gr.Plot(label="Sector Performance")
            benchmark_table = gr.DataFrame(label="Sector Benchmarks")

    # ------------ Event Handlers ------------
    # Single Company Analysis
    single_btn.click(
        fn=lambda c: (analyze_news_sentiment(c), 
                     get_news_previews(c),
        inputs=single_input,
        outputs=[single_output, news_preview]
    )
    
    pdf_btn.click(
        fn=lambda c: export_results.to_pdf(c, analyze_news_sentiment(c)),
        inputs=single_input,
        outputs=gr.File(label="Download PDF")
    )
    
    single_input.change(
        fn=create_historical_comparison,
        inputs=single_input,
        outputs=history_output
    )
    
    # Multi-Company Analysis
    rank_btn.click(
        fn=lambda c,s: (update_ranking(c),
                      generate_sector_report(s)),
        inputs=[multi_input, sector_dropdown],
        outputs=[rank_list, rank_output, sector_chart, benchmark_table]
    )
    
    csv_btn.click(
        fn=lambda c: export_results.to_csv(analyze_multiple_stocks(c.split(','))),
        inputs=multi_input,
        outputs=gr.File(label="Download CSV")
    )
    
    sector_dropdown.change(
        fn=generate_sector_report,
        inputs=sector_dropdown,
        outputs=[sector_chart, benchmark_table]
    )

if __name__ == "__main__":
    interface.launch()