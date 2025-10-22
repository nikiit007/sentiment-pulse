import pandas as pd
from dash import html

def create_negative_sentiment_table(data):
    df = pd.DataFrame(data['character_wow_delta'])
    df['delta'] = df['current'] - df['last_week']
    df_sorted = df.sort_values(by='delta').head(5)

    rows = [html.Tr([html.Th("Character"), html.Th("Current Avg"), html.Th("WoW Delta")])]
    for _, row in df_sorted.iterrows():
        rows.append(html.Tr([
            html.Td(row['character']),
            html.Td(f"{row['current']:.2f}"),
            html.Td(f"{row['delta']:.2f}")
        ]))
    return html.Table(rows)

def create_mentions_list(data):
    mentions = data['mentions_sample'][:10]
    children = []
    for mention in mentions:
        sentiment_color = '#4CAF50' if mention['sentiment'] > 0 else '#f44336' if mention['sentiment'] < 0 else '#757575'
        children.append(html.Div([
            html.Span(f"{mention['platform']}", className=f"platform-badge platform-{mention['platform']}"),
            html.Span(f" {mention['created_at']} "),
            html.Span(f"Sentiment: {mention['sentiment']:.2f}", className="sentiment-chip", style={'backgroundColor': sentiment_color}),
            html.P(mention['text'])
        ], className='mention'))
    return children
