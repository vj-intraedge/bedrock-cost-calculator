"""
Chart components using Plotly.
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from calculator.totals import CostSummary


def render_pie_chart(summary: CostSummary) -> None:
    """Render a pie chart showing cost breakdown by service."""
    breakdown = summary.breakdown_by_service

    # Filter out zero-cost services
    labels = [k for k, v in breakdown.items() if v > 0]
    values = [v for v in breakdown.values() if v > 0]

    if not values:
        st.info("No costs to display.")
        return

    fig = px.pie(
        names=labels,
        values=values,
        title="Cost Breakdown by Service",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        margin=dict(t=50, b=20, l=20, r=20),
        height=350,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_bar_chart(summary: CostSummary) -> None:
    """Render a bar chart showing largest cost contributors."""
    # Sort results by subtotal descending
    sorted_results = sorted(summary.all_results, key=lambda r: r.subtotal, reverse=True)
    top_results = sorted_results[:10]  # Top 10

    labels = [f"{r.service} - {r.component}" for r in top_results]
    values = [r.subtotal for r in top_results]

    fig = go.Figure(data=[
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color=px.colors.qualitative.Set2[:len(values)],
        )
    ])
    fig.update_layout(
        title="Top Cost Contributors",
        xaxis_title="Monthly Cost ($)",
        yaxis=dict(autorange="reversed"),
        margin=dict(t=50, b=40, l=20, r=20),
        height=350,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_monthly_vs_annual(summary: CostSummary) -> None:
    """Render monthly vs annual comparison."""
    fig = go.Figure(data=[
        go.Bar(
            x=["Monthly", "Annual"],
            y=[summary.monthly_total, summary.annual_total],
            marker_color=["#2ecc71", "#3498db"],
            text=[f"${summary.monthly_total:.2f}", f"${summary.annual_total:.2f}"],
            textposition="auto",
        )
    ])
    fig.update_layout(
        title="Monthly vs Annual Cost",
        yaxis_title="Cost ($)",
        margin=dict(t=50, b=40, l=20, r=20),
        height=300,
    )
    st.plotly_chart(fig, use_container_width=True)
