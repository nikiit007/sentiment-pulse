import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc # Added for dark mode toggle

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
def create_topics_bar_chart(data, theme):
    """Create a styled horizontal bar chart for top trending themes."""
    df = pd.DataFrame(data['topics_weekly'])
    fig = px.bar(
        df, x='count', y='topic', orientation='h',
        title='Top Trending Themes (This Week)',
        template='plotly_white', color='count', color_continuous_scale=px.colors.sequential.Viridis
    )
    font_color = '#fff' if theme == 'dark' else '#000'
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', # Transparent background
        font=dict(color=font_color) # White text for dark mode
    )
    return fig

def create_sentiment_heatmap(data, theme):
    """Create a styled heatmap for character sentiment."""
    df = pd.DataFrame(data['character_daily'])
    pivot_df = df.pivot(index='character', columns='date', values='avg_sentiment')
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values, x=pivot_df.columns, y=pivot_df.index,
        colorscale='RdBu', zmid=0
    ))
    font_color = '#fff' if theme == 'dark' else '#000'
    fig.update_layout(
        title='Character Sentiment Heatmap',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', # Transparent background
        font=dict(color=font_color),
        xaxis=dict(linecolor='#fff' if theme == 'dark' else '#000'),
        yaxis=dict(linecolor='#fff' if theme == 'dark' else '#000')
    )
    return fig

def create_episode_sentiment_chart(data, theme):
    """Create a styled line chart for episode sentiment trends."""
    df = pd.DataFrame(data['episodes'])
    fig = px.line(
        df, x='episode_id', y='avg_sentiment',
        title='Episode Sentiment Trend', markers=True,
        template='plotly_dark'
    )
    font_color = '#fff' if theme == 'dark' else '#000'
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', # Transparent background
        font=dict(color=font_color) # White text for dark mode
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
    return dbc.Table(rows, striped=True, bordered=True, hover=True, className="table-light") # Use table-light for better contrast

def create_mentions_card(data):
    """Create a styled, scrollable card for mentions using bubble-style UI."""
    mentions = data['mentions_sample']

    def get_sentiment_pill(sentiment):
        if sentiment > 0.3:
            return html.Span("Positive", className="sentiment-pill positive")
        if sentiment < -0.3:
            return html.Span("Negative", className="sentiment-pill negative")
        return html.Span("Neutral", className="sentiment-pill neutral")

    bubbles = [
        html.Div([
            html.P(mention['text']),
            html.Div([
                get_sentiment_pill(mention['sentiment']),
                html.Span(
                    f"{mention['platform'].capitalize()} · {pd.to_datetime(mention['created_at']).strftime('%b %d, %H:%M')}",
                    className="timestamp"
                )
            ], className="mention-footer")
        ], className="mention-bubble")
        for mention in mentions
    ]

    return dbc.Card([
        dbc.CardHeader("Recent Mentions"),
        dbc.CardBody(html.Div(bubbles, className="mention-card"))
    ], className="h-100 glass-card") # Added glass-card class

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
    className="sidebar glass-panel", # Added glass-panel class
)

# --- Dark Mode Toggle ---
# Placed here to be included in the main layout
theme_toggle = dmc.Switch(
    id="theme-toggle",
    size="lg",
    radius="sm",
    onLabel="🌙",
    offLabel="☀️",
    color="dark",
    checked=True, # Default to dark mode
    style={"position": "fixed", "top": "1.5rem", "right": "1.5rem", "z-index": "101"}
)

content = html.Div(id="page-content", className="content")

app.layout = dmc.MantineProvider(
    id="theme-provider",
    theme={"colorScheme": "dark"}, # Default to dark theme
    withGlobalClasses=True, # Corrected argument
    children=[
        dcc.Location(id="url"),
        sidebar,
        content,
        theme_toggle
    ]
)

# --- Callbacks ---
@app.callback(
    Output("theme-provider", "theme"),
    Input("theme-toggle", "checked")
)
def update_theme(checked):
    """Toggle between light and dark mode."""
    return {"colorScheme": "dark" if checked else "light"}

app.clientside_callback(
    """
    function(theme) {
        if (theme && theme.colorScheme === 'dark') {
            document.body.classList.add('dark-theme');
        } else {
            document.body.classList.remove('dark-theme');
        }
        return '';
    }
    """,
    Output('theme-provider', 'id'), # Dummy output
    Input('theme-provider', 'theme')
)

@app.callback(
    Output("topics-bar-chart", "figure"),
    Output("sentiment-heatmap", "figure"),
    Output("episode-sentiment-chart", "figure"),
    Input("theme-provider", "theme")
)
def update_graphs(theme):
    color_scheme = theme.get("colorScheme", "light")
    return (
        create_topics_bar_chart(data, color_scheme),
        create_sentiment_heatmap(data, color_scheme),
        create_episode_sentiment_chart(data, color_scheme)
    )


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    """Render content based on the URL."""
    if pathname == "/":
        return dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(id="topics-bar-chart"), className="glass-card"), width=12, lg=6),
                dbc.Col(dbc.Card(dcc.Graph(id="sentiment-heatmap"), className="glass-card"), width=12, lg=6),
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(id="episode-sentiment-chart"), className="glass-card"), width=12, lg=6),
                dbc.Col(create_mentions_card(data), width=12, lg=6),
            ]),
        ], fluid=True)
    elif pathname == "/data":
        return dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader("Character Sentiment Breakdown"),
                    dbc.CardBody(create_character_table(data))
                ], className="glass-card"), width=12)
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
    app.run(debug=True, port=8080, host='0.0.0.0')
    