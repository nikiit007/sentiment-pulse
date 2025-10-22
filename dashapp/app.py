import json
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import os

from components.charts import create_topics_bar_chart, create_sentiment_heatmap, create_episode_sentiment_chart
from components.tables import create_negative_sentiment_table, create_mentions_list

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'agg', 'daily.json')

def load_data():
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

data = load_data()

app = Dash(__name__, assets_folder='assets')
server = app.server

app.layout = html.Div([
    html.Div([
        html.H1("Topic Trend & Sentiment Pulse"),
        html.Button("Reload Data", id="reload-button")
    ], className="header"),
    html.Div(id='main-container', className="container")
])

@app.callback(
    Output('main-container', 'children'),
    Input('reload-button', 'n_clicks')
)
def update_layout(n_clicks):
    global data
    if n_clicks and n_clicks > 0:
        data = load_data()

    return [
        html.Div([
            dcc.Graph(figure=create_topics_bar_chart(data))
        ], className="card"),
        html.Div([
            dcc.Graph(figure=create_sentiment_heatmap(data))
        ], className="card"),
        html.Div([
            html.H3("Rising Negative Sentiment"),
            create_negative_sentiment_table(data)
        ], className="card"),
        html.Div([
            dcc.Graph(figure=create_episode_sentiment_chart(data))
        ], className="card"),
        html.Div([
            html.H3("Mentions (Sample)"),
            html.Div(create_mentions_list(data))
        ], className="card"),
    ]

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8050)
