"""
visualization.py
------------------
Builds all charts used in the Streamlit dashboard using Plotly
(interactive) and WordCloud (static image), keeping app.py focused
purely on layout/orchestration.
"""

import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import pandas as pd


# Professional color palette used consistently across all charts
COLOR_SEQUENCE = ["#4F46E5", "#06B6D4", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]


def build_ranking_bar_chart(df: pd.DataFrame):
    """
    Horizontal bar chart of candidates ranked by final match score.

    Args:
        df: ranking DataFrame (output of ranking.build_ranking_table).

    Returns:
        Plotly Figure object.
    """
    fig = px.bar(
        df.sort_values("Match Score (%)", ascending=True),
        x="Match Score (%)",
        y="Candidate",
        orientation="h",
        color="Match Score (%)",
        color_continuous_scale="Blues",
        text="Match Score (%)",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(
        title="Candidate Ranking Overview",
        xaxis_title="Match Score (%)",
        yaxis_title="",
        height=max(350, 45 * len(df)),
        margin=dict(l=10, r=10, t=50, b=10),
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_score_breakdown_chart(candidate_row: dict):
    """
    Pie/donut chart showing the semantic-similarity vs skill-coverage
    breakdown for a single candidate.

    Args:
        candidate_row: a single row (as dict) from the ranking DataFrame.

    Returns:
        Plotly Figure object.
    """
    labels = ["Semantic Similarity", "Skill Coverage"]
    values = [
        candidate_row["Semantic Similarity (%)"],
        candidate_row["Skill Coverage (%)"],
    ]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=[COLOR_SEQUENCE[0], COLOR_SEQUENCE[1]]),
    )])
    fig.update_layout(
        title=f"Score Breakdown — {candidate_row['Candidate']}",
        margin=dict(l=10, r=10, t=50, b=10),
        height=320,
        showlegend=True,
    )
    return fig


def build_skill_comparison_chart(matched_count: int, missing_count: int, candidate_name: str):
    """
    Simple bar chart comparing matched vs missing skill counts for a candidate.

    Args:
        matched_count: number of JD skills found in resume.
        missing_count: number of JD skills missing from resume.
        candidate_name: display name for the chart title.

    Returns:
        Plotly Figure object.
    """
    fig = go.Figure(data=[
        go.Bar(name="Matched", x=["Skills"], y=[matched_count], marker_color=COLOR_SEQUENCE[2]),
        go.Bar(name="Missing", x=["Skills"], y=[missing_count], marker_color=COLOR_SEQUENCE[4]),
    ])
    fig.update_layout(
        barmode="stack",
        title=f"Skill Coverage — {candidate_name}",
        height=300,
        margin=dict(l=10, r=10, t=50, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_wordcloud_image(text: str):
    """
    Generates a WordCloud image object from text (e.g. all resume
    tokens combined) to visually surface dominant themes/skills.

    Args:
        text: space-separated token string.

    Returns:
        A WordCloud object with .to_array() ready for st.image(),
        or None if there isn't enough text to render.
    """
    if not text or not text.strip():
        return None

    wc = WordCloud(
        width=900,
        height=400,
        background_color="white",
        colormap="viridis",
        max_words=80,
    ).generate(text)

    return wc


def build_match_distribution_chart(df: pd.DataFrame):
    """
    Histogram showing the distribution of match scores across all
    candidates — useful for recruiters screening large batches.

    Args:
        df: ranking DataFrame.

    Returns:
        Plotly Figure object.
    """
    fig = px.histogram(
        df,
        x="Match Score (%)",
        nbins=10,
        color_discrete_sequence=[COLOR_SEQUENCE[0]],
    )
    fig.update_layout(
        title="Match Score Distribution",
        xaxis_title="Match Score (%)",
        yaxis_title="Number of Candidates",
        height=320,
        margin=dict(l=10, r=10, t=50, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
