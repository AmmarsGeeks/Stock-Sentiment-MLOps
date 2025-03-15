import plotly.graph_objects as go
import pandas as pd

def create_sentiment_chart(df, company_name):
    """Create interactive sentiment visualization"""
    positive = df[df['sentiment'] == 1]['sentiment']
    negative = df[df['sentiment'] == -1]['sentiment']

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=positive, nbinsx=1, name='Positive',
        marker_color='purple', opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=negative, nbinsx=1, name='Negative',
        marker_color='skyblue', opacity=0.75
    ))

    fig.update_layout(
        title=f'Sentiment Distribution for {company_name}',
        xaxis_title='Sentiment',
        yaxis_title='Count',
        barmode='overlay',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        xaxis=dict(tickvals=[-1, 1], ticktext=['Negative', 'Positive']),
        bargap=0.2,
    )
    return fig