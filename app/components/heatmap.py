"""
Heatmap components for the RiskLens Streamlit app.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src import (
    fetch_ohlcv, get_sector_mapping,
    prepare_cross_sectional_heatmap,
    prepare_sector_volatility_heatmap, prepare_correlation_heatmap,
    create_volatility_heatmap, create_correlation_heatmap,
    compute_sector_correlation, historical_volatility, 
    parkinson_volatility, garman_klass_volatility
)


def render_data_input_section():
    """Render the data input section."""
    st.subheader("📊 Data Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Ticker input options
        input_method = st.radio(
            "How would you like to input tickers?",
            ["Select from predefined lists", "Enter custom tickers"],
            horizontal=True
        )
        
        if input_method == "Select from predefined lists":
            # Import here to avoid circular import
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from config import get_stock_lists
            stock_lists = get_stock_lists()
            
            selected_list = st.selectbox(
                "Choose a stock list:",
                list(stock_lists.keys())
            )
            
            tickers = stock_lists[selected_list]
            st.info(f"Selected tickers: {', '.join(tickers)}")
            
        else:
            ticker_input = st.text_area(
                "Enter tickers (comma-separated):",
                value="AAPL,GOOGL,MSFT,AMZN,TSLA,META,NVDA,NFLX",
                help="Enter stock tickers separated by commas (e.g., AAPL,GOOGL,MSFT)"
            )
            tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
    
    with col2:
        # Date range
        st.write("**Date Range**")
        start_date = st.date_input(
            "Start Date",
            value=pd.to_datetime("2023-01-01"),
            help="Start date for data fetching"
        )
        
        end_date = st.date_input(
            "End Date", 
            value=pd.to_datetime("2024-12-31"),
            help="End date for data fetching"
        )
    
    return tickers, str(start_date), str(end_date)


def render_volatility_parameters():
    """Render volatility calculation parameters."""
    st.subheader("⚙️ Volatility Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        volatility_method = st.selectbox(
            "Volatility Method",
            ["Historical", "Parkinson", "Garman-Klass"],
            help="Select the volatility calculation method"
        )
    
    with col2:
        window = st.number_input(
            "Rolling Window (days)",
            min_value=5,
            max_value=252,
            value=30,
            help="Rolling window for volatility calculation"
        )
    
    with col3:
        annualize = st.checkbox(
            "Annualize Volatility",
            value=True,
            help="Whether to annualize volatility values"
        )
    
    return volatility_method.lower(), window, annualize


def render_heatmap_parameters():
    """Render heatmap visualization parameters."""
    st.subheader("🎨 Heatmap Visualization")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        heatmap_type = st.selectbox(
            "Heatmap Type",
            [
                "Time Series Heatmap",
                "Cross-Sectional Heatmap", 
                "Sector Volatility Heatmap",
                "Correlation Heatmap"
            ],
            help="Select the type of heatmap to generate"
        )
    
    with col2:
        color_scale = st.selectbox(
            "Color Scale",
            ["RdYlBu_r", "Viridis", "Plasma", "Inferno", "RdBu", "Spectral"],
            help="Select the color scale for the heatmap"
        )
    
    with col3:
        show_values = st.checkbox(
            "Show Values",
            value=True,
            help="Whether to display values on the heatmap"
        )
    
    # Additional parameters based on heatmap type
    additional_params = {}
    
    if heatmap_type == "Cross-Sectional Heatmap":
        additional_params['percentile_range'] = st.slider(
            "Percentile Range for Outlier Detection",
            min_value=1,
            max_value=20,
            value=5,
            help="Percentile range for identifying outliers"
        )
    
    elif heatmap_type == "Sector Volatility Heatmap":
        additional_params['aggregation_method'] = st.selectbox(
            "Sector Aggregation Method",
            ["mean", "median", "weighted"],
            help="Method to aggregate stock volatilities into sector volatilities"
        )
    
    return heatmap_type, color_scale, show_values, additional_params


@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_stock_data(tickers: List[str], start_date: str, end_date: str):
    """Fetch stock data with caching."""
    try:
        data = fetch_ohlcv(tickers, start_date, end_date)
        return data
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None


@st.cache_data(ttl=3600)
def get_sectors_for_tickers(tickers: List[str]):
    """Get sector mapping for tickers with caching."""
    try:
        sector_df = get_sector_mapping(tickers)
        if sector_df.empty:
            st.warning(f"No sector data found for tickers: {', '.join(tickers)}")
            return {}
        
        sector_map = dict(zip(sector_df['Ticker'], sector_df['Sector']))
        
        # Log the mapping for debugging
        st.info(f"Sector mapping created for {len(sector_map)} tickers")
        
        return sector_map
    except Exception as e:
        st.error(f"Error fetching sector data: {str(e)}")
        return {}


def generate_heatmap(
    data: pd.DataFrame,
    heatmap_type: str,
    volatility_method: str,
    window: int,
    annualize: bool,
    color_scale: str,
    show_values: bool,
    additional_params: Dict,
    sector_map: Optional[Dict] = None
):
    """Generate the requested heatmap."""
    
    if data is None or data.empty:
        st.error("No data available for heatmap generation")
        return None
    
    try:
        # Generate heatmap data based on type
        if heatmap_type == "Time Series Heatmap":
            # For time series, we need to calculate volatility first then format for heatmap
            volatilities = {}
            tickers = data.index.get_level_values('Ticker').unique()
            
            for ticker in tickers:
                ticker_data = data.xs(ticker, level='Ticker')
                
                if volatility_method.lower() == 'historical':
                    from src.volatility import historical_volatility
                    vol = historical_volatility(ticker_data, window=window, annualize=annualize)
                elif volatility_method.lower() == 'parkinson':
                    from src.volatility import parkinson_volatility
                    vol = parkinson_volatility(ticker_data, window=window, annualize=annualize)
                elif volatility_method.lower() == 'garman-klass':
                    from src.volatility import garman_klass_volatility
                    vol = garman_klass_volatility(ticker_data, window=window, annualize=annualize)
                else:
                    from src.volatility import historical_volatility
                    vol = historical_volatility(ticker_data, window=window, annualize=annualize)
                
                volatilities[ticker] = vol.dropna()
            
            # Create DataFrame with dates as index, tickers as columns
            heatmap_data = pd.DataFrame(volatilities)
            title = f"Time Series Volatility Heatmap ({volatility_method.title()})"
            
        elif heatmap_type == "Cross-Sectional Heatmap":
            heatmap_data = prepare_cross_sectional_heatmap(
                data,
                window=window
            )
            title = f"Cross-Sectional Volatility Heatmap"
            
        elif heatmap_type == "Sector Volatility Heatmap":
            if not sector_map:
                st.error("Sector mapping is required for sector heatmap")
                return None
            
            if len(sector_map) == 0:
                st.error("No sector data available. Please try with different tickers or check your internet connection.")
                return None
            
            # Convert sector_map dict to DataFrame format expected by function
            sector_df = pd.DataFrame(list(sector_map.items()), columns=['Ticker', 'Sector'])
            
            # Debug info
            st.info(f"Processing {len(sector_df)} tickers across {sector_df['Sector'].nunique()} sectors")
            
            heatmap_data = prepare_sector_volatility_heatmap(
                data,
                sector_df,
                window=window
            )
            title = f"Sector Volatility Heatmap"
            
        elif heatmap_type == "Correlation Heatmap":
            heatmap_data = prepare_correlation_heatmap(
                data,
                window=window
            )
            title = "Volatility Correlation Heatmap"
            
            # Use different visualization for correlation
            fig = create_correlation_heatmap(
                heatmap_data,
                title=title,
                height=600
            )
            return fig
        
        else:
            st.error(f"Unsupported heatmap type: {heatmap_type}")
            return None
        
        # Create the visualization
        fig = create_volatility_heatmap(
            heatmap_data,
            title=title,
            color_scale=color_scale,
            show_values=show_values,
            height=600
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error generating heatmap: {str(e)}")
        st.exception(e)  # This will show the full stack trace for debugging
        return None


def render_heatmap_analysis():
    """Render the complete heatmap analysis interface."""
    
    # Data Input Section
    tickers, start_date, end_date = render_data_input_section()
    
    if not tickers:
        st.warning("Please enter at least one ticker symbol")
        return
    
    # Parameters Section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        volatility_method, window, annualize = render_volatility_parameters()
    
    with col2:
        heatmap_type, color_scale, show_values, additional_params = render_heatmap_parameters()
    
    # Generate button
    if st.button("🔥 Generate Heatmap", type="primary", use_container_width=True):
        
        with st.spinner("Fetching data and generating heatmap..."):
            
            # Fetch stock data
            stock_data = fetch_stock_data(tickers, start_date, end_date)
            
            if stock_data is None:
                return
            
            # Get sector mapping if needed
            sector_map = None
            if heatmap_type == "Sector Volatility Heatmap":
                sector_map = get_sectors_for_tickers(tickers)
            
            # Generate heatmap
            fig = generate_heatmap(
                stock_data,
                heatmap_type,
                volatility_method,
                window,
                annualize,
                color_scale,
                show_values,
                additional_params,
                sector_map
            )
            
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)
                
                # Display summary statistics
                render_summary_statistics(stock_data, volatility_method, window, annualize)
            
    
def render_summary_statistics(data: pd.DataFrame, volatility_method: str, window: int, annualize: bool):
    """Render summary statistics below the heatmap."""
    
    st.subheader("📈 Summary Statistics")
    
    try:
        # Calculate volatility statistics for all tickers
        tickers = data.index.get_level_values('Ticker').unique()
        vol_stats = {}
        
        for ticker in tickers:
            ticker_data = data.xs(ticker, level='Ticker')
            
            if volatility_method.lower() == 'historical':
                from src.volatility import historical_volatility
                vol = historical_volatility(ticker_data, window=window, annualize=annualize)
            elif volatility_method.lower() == 'parkinson':
                from src.volatility import parkinson_volatility
                vol = parkinson_volatility(ticker_data, window=window, annualize=annualize)
            elif volatility_method.lower() == 'garman-klass':
                from src.volatility import garman_klass_volatility
                vol = garman_klass_volatility(ticker_data, window=window, annualize=annualize)
            else:
                from src.volatility import historical_volatility
                vol = historical_volatility(ticker_data, window=window, annualize=annualize)
            
            vol_stats[ticker] = vol.dropna()
        
        if vol_stats:
            # Convert to DataFrame for easier statistics
            vol_df = pd.DataFrame(vol_stats)
            
            if not vol_df.empty:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_vol = vol_df.mean().mean()
                    st.metric(
                        "Average Volatility",
                        f"{avg_vol:.3f}" if not pd.isna(avg_vol) else "N/A"
                    )
                
                with col2:
                    max_vol = vol_df.max().max()
                    st.metric(
                        "Maximum Volatility", 
                        f"{max_vol:.3f}" if not pd.isna(max_vol) else "N/A"
                    )
                
                with col3:
                    min_vol = vol_df.min().min()
                    st.metric(
                        "Minimum Volatility",
                        f"{min_vol:.3f}" if not pd.isna(min_vol) else "N/A"
                    )
                
                with col4:
                    std_vol = vol_df.std().mean()
                    st.metric(
                        "Volatility Std Dev",
                        f"{std_vol:.3f}" if not pd.isna(std_vol) else "N/A"
                    )
                
                # Display latest volatility values
                st.subheader("📊 Latest Volatility Values")
                latest_vols = vol_df.iloc[-1].sort_values(ascending=False)
                st.dataframe(latest_vols.to_frame("Volatility").round(4))
        
    except Exception as e:
        st.warning(f"Could not calculate summary statistics: {str(e)}")
        st.exception(e)  # Show full error for debugging
