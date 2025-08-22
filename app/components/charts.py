"""
Chart components for the RiskLens Streamlit app.
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
    historical_volatility, parkinson_volatility, garman_klass_volatility,
    volatility_summary, rank_sectors_by_volatility,
    create_time_series_plot, create_distribution_plot, 
    create_box_plot, create_ranking_chart, create_regime_plot,
    detect_sector_volatility_regimes, compute_sector_volatility
)


def render_volatility_comparison():
    """Render volatility method comparison charts."""
    st.subheader("📊 Volatility Method Comparison")
    
    # Data input
    col1, col2 = st.columns(2)
    
    with col1:
        ticker_input = st.text_input(
            "Enter tickers (comma-separated):",
            value="AAPL,GOOGL,MSFT",
            help="Enter stock tickers to compare volatility methods"
        )
        tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
    
    with col2:
        window = st.slider(
            "Rolling Window (days)",
            min_value=10,
            max_value=100,
            value=30,
            help="Rolling window for volatility calculation"
        )
    
    # Date range
    col3, col4 = st.columns(2)
    with col3:
        start_date = st.date_input(
            "Start Date",
            value=pd.to_datetime("2023-01-01")
        )
    
    with col4:
        end_date = st.date_input(
            "End Date",
            value=pd.to_datetime("2024-12-31")
        )
    
    if st.button("📈 Generate Comparison", type="primary"):
        
        if not tickers:
            st.warning("Please enter at least one ticker")
            return
        
        with st.spinner("Fetching data and calculating volatilities..."):
            
            # Fetch data
            try:
                data = fetch_ohlcv(tickers, str(start_date), str(end_date))
                
                if data is None or data.empty:
                    st.error("Could not fetch data for the specified tickers")
                    return
                
                # Calculate different volatility measures
                vol_methods = {}
                
                for ticker in tickers:
                    try:
                        # Extract ticker data - handle both single and multiple ticker cases
                        if len(tickers) == 1:
                            # For single ticker, the MultiIndex might have different structure
                            if ticker in data.index.get_level_values('Ticker'):
                                ticker_data = data.xs(ticker, level='Ticker')
                            else:
                                # Fallback: assume all data is for this ticker
                                ticker_data = data.reset_index(level='Ticker', drop=True)
                        else:
                            ticker_data = data.xs(ticker, level='Ticker')
                        
                        # Ensure we have the required columns
                        if 'Adj Close' not in ticker_data.columns:
                            st.error(f"Missing 'Adj Close' column for {ticker}. Available columns: {ticker_data.columns.tolist()}")
                            continue
                        
                        # Historical volatility
                        hist_vol = historical_volatility(ticker_data, window=window, annualize=True)
                        
                        # Parkinson volatility (requires High and Low)
                        if 'High' in ticker_data.columns and 'Low' in ticker_data.columns:
                            park_vol = parkinson_volatility(ticker_data, window=window, annualize=True)
                        else:
                            park_vol = hist_vol  # Fallback to historical
                        
                        # Garman-Klass volatility (requires OHLC)
                        required_cols = ['Open', 'High', 'Low', 'Close']
                        if all(col in ticker_data.columns for col in required_cols):
                            gk_vol = garman_klass_volatility(ticker_data, window=window, annualize=True)
                        else:
                            gk_vol = hist_vol  # Fallback to historical
                        
                        vol_methods[f"{ticker}_Historical"] = hist_vol.dropna()
                        vol_methods[f"{ticker}_Parkinson"] = park_vol.dropna()
                        vol_methods[f"{ticker}_GarmanKlass"] = gk_vol.dropna()
                        
                    except Exception as e:
                        st.error(f"Error processing {ticker}: {str(e)}")
                        continue
                
                # Create comparison DataFrame
                vol_df = pd.DataFrame(vol_methods)
                
                if not vol_df.empty:
                    # Time series plot
                    fig_ts = create_time_series_plot(
                        vol_df,
                        title="Volatility Method Comparison Over Time",
                        y_title="Annualized Volatility",
                        height=500
                    )
                    st.plotly_chart(fig_ts, use_container_width=True)
                    
                    # Box plot comparison
                    fig_box = create_box_plot(
                        vol_df,
                        title="Volatility Distribution by Method",
                        height=400
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
                    
                    # Summary statistics
                    st.subheader("📊 Summary Statistics")
                    st.dataframe(vol_df.describe().round(4))
                
            except Exception as e:
                st.error(f"Error in volatility comparison: {str(e)}")


def render_sector_analysis():
    """Render sector-level volatility analysis."""
    st.subheader("🏭 Sector Volatility Analysis")
    
    # Parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Stock list selection
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from config import get_stock_lists
        stock_lists = get_stock_lists()
        
        selected_list = st.selectbox(
            "Choose stock universe:",
            list(stock_lists.keys())
        )
        tickers = stock_lists[selected_list]
    
    with col2:
        aggregation_method = st.selectbox(
            "Aggregation Method",
            ["mean", "median", "weighted"],
            help="Method to aggregate individual stock volatilities into sector volatilities"
        )
    
    with col3:
        top_n = st.number_input(
            "Top N Sectors",
            min_value=3,
            max_value=15,
            value=10,
            help="Number of top volatile sectors to display"
        )
    
    # Date range
    col4, col5 = st.columns(2)
    with col4:
        start_date = st.date_input(
            "Start Date",
            value=pd.to_datetime("2023-01-01"),
            key="sector_start"
        )
    
    with col5:
        end_date = st.date_input(
            "End Date",
            value=pd.to_datetime("2024-12-31"),
            key="sector_end"
        )
    
    if st.button("🏭 Analyze Sectors", type="primary"):
        
        with st.spinner("Fetching data and analyzing sectors..."):
            
            try:
                # Fetch stock data
                data = fetch_ohlcv(tickers, str(start_date), str(end_date))
                
                if data is None or data.empty:
                    st.error("Could not fetch data")
                    return
                
                # Get sector mapping
                sector_map = get_sector_mapping(tickers)
                sector_dict = dict(zip(sector_map['Ticker'], sector_map['Sector']))
                
                # Calculate stock volatilities
                stock_vols = {}
                for ticker in tickers:
                    try:
                        # Extract ticker data - handle both single and multiple ticker cases  
                        if len(tickers) == 1:
                            if ticker in data.index.get_level_values('Ticker'):
                                ticker_data = data.xs(ticker, level='Ticker')
                            else:
                                ticker_data = data.reset_index(level='Ticker', drop=True)
                        else:
                            if ticker in data.index.get_level_values('Ticker'):
                                ticker_data = data.xs(ticker, level='Ticker')
                            else:
                                continue
                        
                        # Ensure we have the required column
                        if 'Adj Close' not in ticker_data.columns:
                            continue
                            
                        vol = historical_volatility(ticker_data, window=30, annualize=True)
                        stock_vols[ticker] = vol.dropna()
                        
                    except Exception as e:
                        st.warning(f"Could not process {ticker}: {str(e)}")
                        continue
                
                if stock_vols:
                    # Convert to DataFrame with proper structure
                    # Each column should be a ticker, each row should be a date
                    max_length = max(len(vol) for vol in stock_vols.values())
                    aligned_vols = {}
                    
                    for ticker, vol_series in stock_vols.items():
                        if len(vol_series) == max_length:
                            aligned_vols[ticker] = vol_series.values
                        else:
                            # Pad shorter series with NaN
                            padded = np.full(max_length, np.nan)
                            padded[:len(vol_series)] = vol_series.values
                            aligned_vols[ticker] = padded
                    
                    # Get the most recent date index from the longest series
                    longest_series = max(stock_vols.values(), key=len)
                    stock_vol_df = pd.DataFrame(aligned_vols, index=longest_series.index)
                    
                    # Calculate sector volatilities
                    sector_vols = compute_sector_volatility(
                        stock_vol_df,  # DataFrame with dates as index, tickers as columns
                        sector_dict,
                        method=aggregation_method
                    )
                    
                    if not sector_vols.empty:
                        st.success(f"✅ Analyzed {len(stock_vols)} stocks across {len(sector_vols.columns)} sectors")
                        
                        # Rank sectors by latest volatility
                        latest_volatilities = sector_vols.iloc[-1]
                        ranking_df = latest_volatilities.sort_values(ascending=False).head(top_n).to_frame()
                        ranking_df.columns = ['Volatility']
                        
                        # Create ranking chart
                        fig_ranking = create_ranking_chart(
                            ranking_df,
                            title=f"Top {top_n} Most Volatile Sectors",
                            height=500
                        )
                        st.plotly_chart(fig_ranking, use_container_width=True)
                        
                        # Time series of sector volatilities
                        fig_ts = create_time_series_plot(
                            sector_vols,
                            title="Sector Volatility Over Time",
                            y_title="Volatility",
                            height=500
                        )
                        st.plotly_chart(fig_ts, use_container_width=True)
                        
                        # Volatility regime detection
                        try:
                            regimes = detect_sector_volatility_regimes(
                                sector_vols,
                                thresholds=(0.15, 0.30)
                            )
                            
                            if not regimes.empty:
                                fig_regime = create_regime_plot(
                                    regimes,
                                    sector_vols,
                                    title="Sector Volatility Regimes",
                                    height=600
                                )
                                st.plotly_chart(fig_regime, use_container_width=True)
                        except Exception as e:
                            st.info(f"Regime detection not available: {str(e)}")
                        
                        # Display sector statistics
                        st.subheader("📊 Sector Statistics")
                        stats_df = sector_vols.describe()
                        st.dataframe(stats_df, use_container_width=True)
                    else:
                        st.warning("No sector volatility data could be computed")
                else:
                    st.warning("No stock volatility data available for analysis")
                
            except Exception as e:
                st.error(f"Error in sector analysis: {str(e)}")
                st.error(f"Debug info: {e.__class__.__name__}")


def render_distribution_analysis():
    """Render volatility distribution analysis."""
    st.subheader("📊 Volatility Distribution Analysis")
    
    # Parameters
    col1, col2 = st.columns(2)
    
    with col1:
        ticker_input = st.text_input(
            "Enter tickers (comma-separated):",
            value="AAPL,GOOGL,MSFT,AMZN,TSLA",
            help="Enter stock tickers for distribution analysis",
            key="dist_tickers"
        )
        tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
    
    with col2:
        volatility_method = st.selectbox(
            "Volatility Method",
            ["Historical", "Parkinson", "Garman-Klass"],
            key="dist_method"
        )
    
    # Date range
    col3, col4 = st.columns(2)
    with col3:
        start_date = st.date_input(
            "Start Date",
            value=pd.to_datetime("2023-01-01"),
            key="dist_start"
        )
    
    with col4:
        end_date = st.date_input(
            "End Date",
            value=pd.to_datetime("2024-12-31"),
            key="dist_end"
        )
    
    if st.button("📈 Analyze Distributions", type="primary"):
        
        with st.spinner("Calculating volatility distributions..."):
            
            try:
                # Fetch data
                data = fetch_ohlcv(tickers, str(start_date), str(end_date))
                
                if data is None or data.empty:
                    st.error("Could not fetch data")
                    return
                
                # Calculate volatilities
                volatilities = {}
                
                for ticker in tickers:
                    try:
                        # Extract ticker data - handle both single and multiple ticker cases
                        if len(tickers) == 1:
                            # For single ticker, the MultiIndex might have different structure
                            if ticker in data.index.get_level_values('Ticker'):
                                ticker_data = data.xs(ticker, level='Ticker')
                            else:
                                # Fallback: assume all data is for this ticker
                                ticker_data = data.reset_index(level='Ticker', drop=True)
                        else:
                            if ticker in data.index.get_level_values('Ticker'):
                                ticker_data = data.xs(ticker, level='Ticker')
                            else:
                                st.warning(f"Data not found for {ticker}")
                                continue
                        
                        # Ensure we have the required columns
                        if 'Adj Close' not in ticker_data.columns:
                            st.error(f"Missing 'Adj Close' column for {ticker}. Available columns: {ticker_data.columns.tolist()}")
                            continue
                        
                        # Calculate volatility based on selected method
                        if volatility_method == "Historical":
                            vol = historical_volatility(ticker_data, window=30, annualize=True)
                        elif volatility_method == "Parkinson":
                            if 'High' in ticker_data.columns and 'Low' in ticker_data.columns:
                                vol = parkinson_volatility(ticker_data, window=30, annualize=True)
                            else:
                                st.warning(f"Missing High/Low data for {ticker}, using Historical method")
                                vol = historical_volatility(ticker_data, window=30, annualize=True)
                        else:  # Garman-Klass
                            required_cols = ['Open', 'High', 'Low', 'Close']
                            if all(col in ticker_data.columns for col in required_cols):
                                vol = garman_klass_volatility(ticker_data, window=30, annualize=True)
                            else:
                                st.warning(f"Missing OHLC data for {ticker}, using Historical method")
                                vol = historical_volatility(ticker_data, window=30, annualize=True)
                        
                        volatilities[ticker] = vol.dropna()
                        
                    except Exception as e:
                        st.error(f"Error processing {ticker}: {str(e)}")
                        continue
                
                if volatilities:
                    vol_df = pd.DataFrame(volatilities)
                    
                    # Individual distribution plots
                    for ticker in tickers[:4]:  # Limit to first 4 tickers
                        if ticker in vol_df.columns:
                            fig_dist = create_distribution_plot(
                                vol_df[ticker],
                                title=f"{ticker} Volatility Distribution ({volatility_method})",
                                bins=30
                            )
                            st.plotly_chart(fig_dist, use_container_width=True)
                    
                    # Comparative box plot
                    fig_box = create_box_plot(
                        vol_df,
                        title=f"Volatility Distribution Comparison ({volatility_method})",
                        height=500
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
                    
                    # Summary statistics
                    st.subheader("📊 Distribution Statistics")
                    stats_df = vol_df.describe().round(4)
                    st.dataframe(stats_df)
                    
                    # Correlation analysis
                    if len(vol_df.columns) > 1:
                        corr_matrix = vol_df.corr()
                        st.subheader("🔗 Volatility Correlations")
                        st.dataframe(corr_matrix.round(3))
                
            except Exception as e:
                st.error(f"Error in distribution analysis: {str(e)}")


def render_chart_analysis():
    """Render the complete chart analysis interface."""
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Volatility Comparison", 
        "🏭 Sector Analysis", 
        "📈 Distribution Analysis"
    ])
    
    with tab1:
        render_volatility_comparison()
    
    with tab2:
        render_sector_analysis()
    
    with tab3:
        render_distribution_analysis()
