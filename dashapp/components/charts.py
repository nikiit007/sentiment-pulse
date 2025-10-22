import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_topics_bar_chart(data):
    df = pd.DataFrame(data['topics_weekly'])
    fig = px.bar(df, x='count', y='topic', orientation='h', title='Top Trending Themes (This Week)')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def create_sentiment_heatmap(data):
    df = pd.DataFrame(data['character_daily'])
    pivot_df = df.pivot(index='character', columns='date', values='avg_sentiment')
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='RdBu',
        zmid=0
    ))
    fig.update_layout(title='Character Sentiment Heatmap')
    return fig

def create_episode_sentiment_chart(data):
    df = pd.DataFrame(data['episodes'])
    fig = px.line(df, x='episode_id', y='avg_sentiment', title='Episode Sentiment Trend', markers=True)
    return fig
