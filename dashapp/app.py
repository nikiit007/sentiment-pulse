import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# --- Configuration & Data Loading ---
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'agg', 'daily.json')
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.15.4/css/all.css"

def load_data():
    """Load data from the JSON file."""
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

data = load_data()

# --- Initialize Dash App ---
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME],
    suppress_callback_exceptions=True
)
server = app.server

# --- Reusable Chart and Table Functions ---
def create_topics_bar_chart(data):
    """Create a styled horizontal bar chart for top trending themes."""
    df = pd.DataFrame(data['topics_weekly'])
    fig = px.bar(
        df, x='count', y='topic', orientation='h',
        title='Top Trending Themes (This Week)',
        template='plotly_white', color='count', color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        paper_bgcolor='#fff', plot_bgcolor='#fff',
        font=dict(color='#333')
    )
    return fig

def create_sentiment_heatmap(data):
    """Create a styled heatmap for character sentiment."""
    df = pd.DataFrame(data['character_daily'])
    pivot_df = df.pivot(index='character', columns='date', values='avg_sentiment')
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values, x=pivot_df.columns, y=pivot_df.index,
        colorscale='RdBu', zmid=0
    ))
    fig.update_layout(
        title='Character Sentiment Heatmap',
        template='plotly_white',
        paper_bgcolor='#fff', plot_bgcolor='#fff',
        font=dict(color='#333')
    )
    return fig

def create_episode_sentiment_chart(data):
    """Create a styled line chart for episode sentiment trends."""
    df = pd.DataFrame(data['episodes'])
    fig = px.line(
        df, x='episode_id', y='avg_sentiment',
        title='Episode Sentiment Trend', markers=True,
        template='plotly_dark'
    )
    fig.update_layout(
        template='plotly_white',
        paper_bgcolor='#fff', plot_bgcolor='#fff',
        font=dict(color='#333')
    )
    return fig

def create_character_table(data):
    """Create a styled table for character sentiment with conditional formatting."""
    df = pd.DataFrame(data['character_wow_delta'])
    df['delta'] = df['current'] - df['last_week']
    df = df.sort_values(by='delta')

    def get_color(value):
        return 'sentiment-negative' if value < 0 else 'sentiment-positive'

    rows = [
        html.Tr([
            html.Th("Character"),
            html.Th("Current Avg"),
            html.Th("WoW Delta")
        ])
    ]
    for _, row in df.iterrows():
        rows.append(html.Tr([
            html.Td(row['character']),
            html.Td(f"{row['current']:.2f}", className=get_color(row['current'])),
            html.Td(f"{row['delta']:.2f}", className=get_color(row['delta']))
        ]))
    return dbc.Table(rows, striped=True, bordered=True, hover=True, className="table-dark")

def create_mentions_card(data):
    """Create a styled, scrollable card for mentions."""
    mentions = data['mentions_sample']

    def get_sentiment_badge(sentiment):
        if sentiment > 0.3:
            return dbc.Badge("Positive", color="success", className="ml-1")
        if sentiment < -0.3:
            return dbc.Badge("Negative", color="danger", className="ml-1")
        return dbc.Badge("Neutral", color="secondary", className="ml-1")

    return dbc.Card([
        dbc.CardHeader("Recent Mentions"),
        dbc.CardBody([
            html.Div([
                html.Div([
                    html.Div([
                        html.Span(mention['platform'].capitalize(), className=f"platform-badge platform-{mention['platform']}"),
                        html.Span(f" {pd.to_datetime(mention['created_at']).strftime('%Y-%m-%d %H:%M')}", className="text-muted small"),
                        get_sentiment_badge(mention['sentiment'])
                    ], className="mention-header"),
                    html.P(mention['text'], className="mb-0")
                ], className="mention")
                for mention in mentions
            ], className="mention-card")
        ])
    ], className="h-100")

# --- App Layout ---
sidebar = html.Div(
    [
        html.Div(
            [
                html.I(className="fas fa-chart-line fa-2x"),
                html.H2("Sentiment Pulse", className="ml-2"),
            ],
            className="sidebar-header d-flex align-items-center justify-content-center"
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink([html.I(className="fas fa-tachometer-alt mr-2"), "Dashboard"], href="/", active="exact"),
                dbc.NavLink([html.I(className="fas fa-table mr-2"), "Data"], href="/data", active="exact"),
            ],
            vertical=True, pills=True,
        ),
    ],
    className="sidebar",
)

content = html.Div(id="page-content", className="content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# --- Callbacks ---
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    """Render content based on the URL."""
    if pathname == "/":
        return dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(figure=create_topics_bar_chart(data))), width=12, lg=6),
                dbc.Col(dbc.Card(dcc.Graph(figure=create_sentiment_heatmap(data))), width=12, lg=6),
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(figure=create_episode_sentiment_chart(data))), width=12, lg=6),
                dbc.Col(create_mentions_card(data), width=12, lg=6),
            ]),
        ], fluid=True)
    elif pathname == "/data":
        return dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader("Character Sentiment Breakdown"),
                    dbc.CardBody(create_character_table(data))
                ]), width=12)
            ])
        ], fluid=True)
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True, port=8050)