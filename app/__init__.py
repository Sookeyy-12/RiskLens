"""
RiskLens Streamlit Application

A comprehensive volatility analysis dashboard providing:
- Interactive volatility heatmaps
- Multi-method volatility calculations  
- Sector-level risk analysis
- Statistical distribution analysis
- Correlation and regime detection

Usage:
    streamlit run app/main.py
"""

__version__ = "1.0.0"
__author__ = "RiskLens Team"

# Import main components
from .main import main
from .config import configure_streamlit, DEFAULT_PARAMS, STOCK_LISTS

__all__ = [
    'main',
    'configure_streamlit', 
    'DEFAULT_PARAMS',
    'STOCK_LISTS'
]
