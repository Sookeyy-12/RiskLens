"""
Configuration settings for the RiskLens Streamlit app.
"""

import streamlit as st


# App Configuration
APP_CONFIG = {
    "page_title": "RiskLens - Volatility Analysis Dashboard",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Dark theme configuration
DARK_THEME = {
    "backgroundColor": "#0e1117",
    "secondaryBackgroundColor": "#262730",
    "textColor": "#fafafa",
    "primaryColor": "#ff6b6b"
}

# Default parameters
DEFAULT_PARAMS = {
    "tickers": ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "NFLX"],
    "volatility_window": 30,
    "start_date": "2023-01-01",
    "end_date": "2024-12-31",
    "volatility_methods": [
        "Historical Volatility",
        "Parkinson Volatility", 
        "Garman-Klass Volatility"
    ],
    "heatmap_types": [
        "Time Series Heatmap",
        "Cross-Sectional Heatmap", 
        "Sector Volatility Heatmap",
        "Correlation Heatmap"
    ],
    "color_scales": [
        "RdYlBu_r", "Viridis", "Plasma", "Inferno", 
        "RdBu", "RdYlGn", "Spectral", "Turbo"
    ],
    "aggregation_methods": ["mean", "median", "weighted"],
    "sectors": [
        "Technology", "Healthcare", "Financials", "Consumer Discretionary",
        "Communication Services", "Industrials", "Consumer Staples", 
        "Energy", "Utilities", "Real Estate", "Materials"
    ]
}

# Popular stock lists
STOCK_LISTS = {
    "S&P 500 Tech": ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "NFLX", "CRM", "ADBE"],
    "Dow Jones": ["AAPL", "MSFT", "JPM", "JNJ", "WMT", "PG", "UNH", "HD", "DIS", "BA"],
    "FAANG": ["META", "AAPL", "AMZN", "NFLX", "GOOGL"],
    "Crypto ETFs": ["BTC-USD", "ETH-USD", "ADA-USD", "DOT-USD", "LINK-USD"],
    "Banking": ["JPM", "BAC", "WFC", "C", "GS", "MS", "USB", "PNC"],
    "Energy": ["XOM", "CVX", "COP", "EOG", "SLB", "MPC", "PSX", "VLO"],
    "Healthcare": ["JNJ", "PFE", "MRK", "ABBV", "TMO", "ABT", "DHR", "BMY"]
}

# Chart styling
CHART_STYLE = {
    "template": "plotly_dark",
    "color_discrete_sequence": [
        "#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", 
        "#feca57", "#ff9ff3", "#54a0ff", "#5f27cd"
    ],
    "height": 600,
    "margin": {"l": 60, "r": 60, "t": 60, "b": 60}
}


def configure_streamlit():
    """Configure Streamlit page settings."""
    st.set_page_config(**APP_CONFIG)
    
    # Custom CSS for dark theme
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        .stSelectbox > div > div > select {
            background-color: #262730;
            color: #fafafa;
        }
        
        .stMultiSelect > div > div > div {
            background-color: #262730;
        }
        
        .stDateInput > div > div > input {
            background-color: #262730;
            color: #fafafa;
        }
        
        .stNumberInput > div > div > input {
            background-color: #262730;
            color: #fafafa;
        }
        
        .stSlider > div > div > div {
            background-color: #262730;
        }
        
        h1 {
            color: #ff6b6b;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        h2 {
            color: #4ecdc4;
            margin-top: 2rem;
        }
        
        h3 {
            color: #45b7d1;
        }
        
        .metric-card {
            background-color: #262730;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #ff6b6b;
        }
        
        .info-box {
            background-color: #1f2937;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #374151;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)


def get_default_tickers():
    """Get default ticker list."""
    return DEFAULT_PARAMS["tickers"]


def get_stock_lists():
    """Get predefined stock lists."""
    return STOCK_LISTS
