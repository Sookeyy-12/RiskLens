"""
Home page for the RiskLens Streamlit app.
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import configure_streamlit


def render_home_page():
    """Render the home page with app overview and navigation."""
    
    # Hero section
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #ff6b6b; font-size: 3rem; margin-bottom: 1rem;">
            🔥 RiskLens
        </h1>
        <h2 style="color: #4ecdc4; font-size: 1.5rem; margin-bottom: 2rem;">
            Advanced Volatility Analysis Dashboard
        </h2>
        <p style="font-size: 1.2rem; color: #fafafa; max-width: 800px; margin: 0 auto;">
            Comprehensive volatility heatmaps, sector analysis, and risk metrics 
            for quantitative finance professionals and researchers.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features overview
    st.markdown("---")
    st.subheader("🚀 Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h3 style="color: #ff6b6b;">🔥 Volatility Heatmaps</h3>
            <ul>
                <li>Time Series Heatmaps</li>
                <li>Cross-Sectional Analysis</li>
                <li>Sector Volatility Maps</li>
                <li>Correlation Heatmaps</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h3 style="color: #4ecdc4;">📊 Multiple Volatility Models</h3>
            <ul>
                <li>Historical Volatility</li>
                <li>Parkinson Estimator</li>
                <li>Garman-Klass Estimator</li>
                <li>Beta-Adjusted Volatility</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box">
            <h3 style="color: #45b7d1;">🏭 Sector Analysis</h3>
            <ul>
                <li>Sector Risk Contribution</li>
                <li>Volatility Rankings</li>
                <li>Regime Detection</li>
                <li>Correlation Analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation guide
    st.markdown("---")
    st.subheader("🗺️ Navigation Guide")
    
    nav_col1, nav_col2 = st.columns(2)
    
    with nav_col1:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #ff6b6b;">🔥 Heatmap Analysis</h4>
            <p>Generate interactive volatility heatmaps with customizable parameters:</p>
            <ul>
                <li>Select from predefined stock lists or enter custom tickers</li>
                <li>Choose volatility calculation methods</li>
                <li>Customize visualization parameters</li>
                <li>Export and analyze results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with nav_col2:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #4ecdc4;">📊 Chart Analysis</h4>
            <p>Deep dive into volatility patterns with advanced charts:</p>
            <ul>
                <li>Compare different volatility methods</li>
                <li>Analyze sector-level volatility</li>
                <li>Study volatility distributions</li>
                <li>Identify market regimes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start
    st.markdown("---")
    st.subheader("⚡ Quick Start")
    
    st.markdown("""
    <div class="info-box">
        <ol>
            <li><strong>Navigate to Heatmap Analysis</strong> - Start with the heatmap page for visual volatility analysis</li>
            <li><strong>Select Your Data</strong> - Choose from predefined stock lists or enter custom tickers</li>
            <li><strong>Configure Parameters</strong> - Set volatility method, rolling window, and visualization options</li>
            <li><strong>Generate Analysis</strong> - Click the generate button to create interactive visualizations</li>
            <li><strong>Explore Charts</strong> - Use the Chart Analysis page for deeper statistical insights</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Technical details
    st.markdown("---")
    st.subheader("🔧 Technical Details")
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #45b7d1;">Data Sources</h4>
            <ul>
                <li>Yahoo Finance (yfinance)</li>
                <li>Real-time and historical data</li>
                <li>OHLCV data for volatility calculation</li>
                <li>Sector mapping from company fundamentals</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col2:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #96ceb4;">Volatility Methods</h4>
            <ul>
                <li><strong>Historical:</strong> Traditional close-to-close returns</li>
                <li><strong>Parkinson:</strong> High-low range estimator</li>
                <li><strong>Garman-Klass:</strong> OHLC-based estimator</li>
                <li><strong>Sector:</strong> Aggregated stock-level volatilities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>Built with ❤️ using Streamlit, Plotly, and the RiskLens quantitative finance library by Suket Kamboj.</p>
        <p>For support and documentation, visit the project repository</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    configure_streamlit()
    render_home_page()
