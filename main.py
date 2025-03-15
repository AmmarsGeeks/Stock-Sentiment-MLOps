# main.py
import gradio as gr
from src.app import analyze_news_sentiment, analyze_multiple_stocks

with gr.Blocks() as interface:
    gr.Markdown("# Stock Analysis System")
    
    with gr.Tab("Individual Analysis"):
        with gr.Row():
            single_company_input = gr.Textbox(label="Enter Company Name")
            single_submit = gr.Button("Analyze")
        single_output = gr.Plot(label="Sentiment Distribution")
    
    with gr.Tab("Multi-Company Ranking"):
        with gr.Row():
            multi_company_input = gr.Textbox(label="Enter Companies (comma-separated)")
            rank_submit = gr.Button("Rank")
        rank_output = gr.Textbox(label="Ranking Results")
    
    # Individual analysis handler
    single_submit.click(
        fn=analyze_news_sentiment,
        inputs=single_company_input,
        outputs=single_output
    )
    
    # Ranking handler
    rank_submit.click(
        fn=lambda companies: "\n".join(
            [f"{i+1}. {company}: {score:.2f}" 
             for i, (company, score) in enumerate(analyze_multiple_stocks(companies))]
        ),
        inputs=multi_company_input,
        outputs=rank_output
    )

if __name__ == "__main__":
    interface.launch()