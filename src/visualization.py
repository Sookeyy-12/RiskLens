"""
Visualization utilities for RiskLens volatility analysis.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Tuple, Any
import streamlit as st


def create_volatility_heatmap(
    data: pd.DataFrame,
    title: str = "Volatility Heatmap",
    color_scale: str = "RdYlBu_r",
    show_values: bool = True,
    height: int = 600
) -> go.Figure:
    """
    Create an interactive heatmap for volatility data.
    
    Args:
        data: DataFrame with dates as index and tickers/sectors as columns
        title: Title for the heatmap
        color_scale: Plotly color scale name
        show_values: Whether to show values on heatmap
        height: Height of the figure
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale=color_scale,
        showscale=True,
        text=data.values if show_values else None,
        texttemplate="%{text:.3f}" if show_values else None,
        textfont={"size": 10},
        hoverongaps=False,
        colorbar=dict(
            title=dict(
                text="Volatility",
                side="right"
            )
        )
    ))
    
    fig.update_layout(
        title=title,
        title_x=0.5,
        xaxis_title="Assets/Sectors",
        yaxis_title="Date",
        height=height,
        template="plotly_dark",
        font=dict(color="white")
    )
    
    return fig


def create_correlation_heatmap(
    corr_matrix: pd.DataFrame,
    title: str = "Correlation Matrix",
    height: int = 600
) -> go.Figure:
    """
    Create a correlation heatmap.
    
    Args:
        corr_matrix: Correlation matrix DataFrame
        title: Title for the heatmap
        height: Height of the figure
    
    Returns:
        Plotly figure object
    """
    # Create mask for upper triangle
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    masked_corr = corr_matrix.copy()
    masked_corr[mask] = np.nan
    
    fig = go.Figure(data=go.Heatmap(
        z=masked_corr.values,
        x=masked_corr.columns,
        y=masked_corr.index,
        colorscale="RdBu",
        zmid=0,
        showscale=True,
        text=masked_corr.values,
        texttemplate="%{text:.3f}",
        textfont={"size": 10},
        hoverongaps=False,
        colorbar=dict(
            title=dict(
                text="Correlation",
                side="right"
            )
        )
    ))
    
    fig.update_layout(
        title=title,
        title_x=0.5,
        height=height,
        template="plotly_dark",
        font=dict(color="white")
    )
    
    return fig


def create_time_series_plot(
    data: pd.DataFrame,
    title: str = "Time Series",
    y_title: str = "Value",
    height: int = 400
) -> go.Figure:
    """
    Create a time series plot for multiple series.
    
    Args:
        data: DataFrame with dates as index and series as columns
        title: Title for the plot
        y_title: Y-axis title
        height: Height of the figure
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    for col in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[col],
            mode='lines',
            name=col,
            line=dict(width=2)
        ))
    
    fig.update_layout(
        title=title,
        title_x=0.5,
        xaxis_title="Date",
        yaxis_title=y_title,
        height=height,
        template="plotly_dark",
        font=dict(color="white"),
        hovermode='x unified'
    )
    
    return fig


def create_distribution_plot(
    data: pd.Series,
    title: str = "Distribution",
    bins: int = 50
) -> go.Figure:
    """
    Create a distribution plot with histogram and density.
    
    Args:
        data: Series of values
        title: Title for the plot
        bins: Number of bins for histogram
    
    Returns:
        Plotly figure object
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Histogram
    fig.add_trace(
        go.Histogram(
            x=data,
            nbinsx=bins,
            name="Histogram",
            opacity=0.7,
            yaxis="y1"
        ),
        secondary_y=False,
    )
    
    # Add density line if possible
    try:
        from scipy import stats
        density = stats.gaussian_kde(data.dropna())
        x_range = np.linspace(data.min(), data.max(), 100)
        y_density = density(x_range)
        
        fig.add_trace(
            go.Scatter(
                x=x_range,
                y=y_density,
                mode="lines",
                name="Density",
                line=dict(color="orange", width=3),
                yaxis="y2"
            ),
            secondary_y=True,
        )
    except ImportError:
        pass
    
    fig.update_layout(
        title=title,
        title_x=0.5,
        template="plotly_dark",
        font=dict(color="white")
    )
    
    fig.update_xaxes(title_text="Value")
    fig.update_yaxes(title_text="Frequency", secondary_y=False)
    fig.update_yaxes(title_text="Density", secondary_y=True)
    
    return fig


def create_box_plot(
    data: pd.DataFrame,
    title: str = "Box Plot",
    height: int = 400
) -> go.Figure:
    """
    Create a box plot for comparing distributions.
    
    Args:
        data: DataFrame with columns to compare
        title: Title for the plot
        height: Height of the figure
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    for col in data.columns:
        fig.add_trace(go.Box(
            y=data[col],
            name=col,
            boxpoints='outliers'
        ))
    
    fig.update_layout(
        title=title,
        title_x=0.5,
        yaxis_title="Value",
        height=height,
        template="plotly_dark",
        font=dict(color="white")
    )
    
    return fig


def create_ranking_chart(
    rankings: pd.DataFrame,
    title: str = "Volatility Rankings",
    height: int = 400
) -> go.Figure:
    """
    Create a bar chart for rankings.
    
    Args:
        rankings: DataFrame with assets/sectors and their rankings
        title: Title for the chart
        height: Height of the figure
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure(data=[
        go.Bar(
            x=rankings.index,
            y=rankings.iloc[:, 0],
            text=rankings.iloc[:, 0],
            texttemplate='%{text:.3f}',
            textposition='outside',
            marker_color=px.colors.qualitative.Set3
        )
    ])
    
    fig.update_layout(
        title=title,
        title_x=0.5,
        xaxis_title="Assets/Sectors",
        yaxis_title="Volatility",
        height=height,
        template="plotly_dark",
        font=dict(color="white")
    )
    
    fig.update_xaxes(tickangle=45)
    
    return fig


def create_regime_plot(
    regime_data: pd.DataFrame,
    volatility_data: pd.DataFrame,
    title: str = "Volatility Regimes",
    height: int = 500
) -> go.Figure:
    """
    Create a plot showing volatility regimes over time.
    
    Args:
        regime_data: DataFrame with regime classifications
        volatility_data: DataFrame with actual volatility values
        title: Title for the plot
        height: Height of the figure
    
    Returns:
        Plotly figure object
    """
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=('Volatility Regimes', 'Volatility Values'),
        vertical_spacing=0.1
    )
    
    # Regime plot
    for col in regime_data.columns:
        fig.add_trace(
            go.Scatter(
                x=regime_data.index,
                y=regime_data[col],
                mode='markers+lines',
                name=f"{col} Regime",
                line=dict(width=2)
            ),
            row=1, col=1
        )
    
    # Volatility plot
    for col in volatility_data.columns:
        fig.add_trace(
            go.Scatter(
                x=volatility_data.index,
                y=volatility_data[col],
                mode='lines',
                name=f"{col} Vol",
                line=dict(width=1, dash='dot')
            ),
            row=2, col=1
        )
    
    fig.update_layout(
        title=title,
        title_x=0.5,
        height=height,
        template="plotly_dark",
        font=dict(color="white"),
        hovermode='x unified'
    )
    
    return fig
