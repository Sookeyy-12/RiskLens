"""
Chart analysis page for the RiskLens Streamlit app.
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import configure_streamlit
from components.charts import render_chart_analysis


def render_chart_page():
    """Render the chart analysis page."""
    
    # Page header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #4ecdc4;">📊 Advanced Chart Analysis</h1>
        <p style="color: #fafafa; font-size: 1.1rem;">
            Deep dive into volatility patterns with comprehensive statistical analysis and interactive charts
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions
    with st.expander("📖 Chart Analysis Guide", expanded=False):
        st.markdown("""
        ### Analysis Types Available:
        
        #### 📊 Volatility Comparison
        - Compare different volatility calculation methods side-by-side
        - Time series plots showing how methods differ over time
        - Box plots for distribution comparison
        - Summary statistics for each method
        
        #### 🏭 Sector Analysis
        - Aggregate individual stock volatilities into sector-level metrics
        - Rank sectors by volatility levels
        - Detect volatility regimes (low, medium, high)
        - Time series analysis of sector volatility evolution
        
        #### 📈 Distribution Analysis
        - Study the statistical distribution of volatility values
        - Compare distributions across different assets
        - Identify outliers and extreme values
        - Correlation analysis between asset volatilities
        
        ### Best Practices:
        - Use multiple volatility methods to confirm patterns
        - Consider sector analysis for portfolio-level insights
        - Look for regime changes in volatility patterns
        - Cross-validate findings across different time periods
        """)
    
    # Main chart analysis interface
    render_chart_analysis()
    
    # Additional resources
    st.markdown("---")
    st.subheader("📚 Analysis Interpretation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #ff6b6b;">Volatility Methods</h4>
            <ul>
                <li><strong>Historical:</strong> Based on close-to-close returns, captures overnight gaps</li>
                <li><strong>Parkinson:</strong> Uses high-low range, more efficient for intraday volatility</li>
                <li><strong>Garman-Klass:</strong> Incorporates OHLC, accounts for intraday and overnight moves</li>
            </ul>
            <p><em>Generally: Garman-Klass > Parkinson > Historical in terms of efficiency</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #96ceb4;">Regime Detection</h4>
            <ul>
                <li><strong>Low Regime:</strong> Volatility < 15% (typically stable markets)</li>
                <li><strong>Medium Regime:</strong> 15% < Volatility < 30% (normal market stress)</li>
                <li><strong>High Regime:</strong> Volatility > 30% (crisis or major events)</li>
            </ul>
            <p><em>Thresholds can be customized based on your analysis needs</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer tips
    st.markdown("---")
    st.info("""
    💡 **Pro Tip**: Use the sector analysis to understand which industries are driving overall market volatility. 
    Cross-reference with news events to identify fundamental drivers of volatility spikes.
    """)


if __name__ == "__main__":
    configure_streamlit()
    render_chart_page()
