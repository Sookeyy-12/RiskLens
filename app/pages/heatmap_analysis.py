"""
Heatmap analysis page for the RiskLens Streamlit app.
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import configure_streamlit
from components.heatmap import render_heatmap_analysis


def render_heatmap_page():
    """Render the heatmap analysis page."""
    
    # Page header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #ff6b6b;">🔥 Volatility Heatmap Analysis</h1>
        <p style="color: #fafafa; font-size: 1.1rem;">
            Generate interactive volatility heatmaps with customizable parameters and advanced visualizations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions
    with st.expander("📖 How to Use This Page", expanded=False):
        st.markdown("""
        ### Step-by-Step Guide:
        
        1. **📊 Data Configuration**: Choose your stock universe
           - Select from predefined lists (FAANG, S&P 500 Tech, etc.)
           - Or enter custom ticker symbols
           - Set your analysis date range
        
        2. **⚙️ Volatility Parameters**: Configure calculation settings
           - Choose volatility method (Historical, Parkinson, Garman-Klass)
           - Set rolling window for calculations
           - Option to annualize volatility values
        
        3. **🎨 Heatmap Visualization**: Customize the display
           - Select heatmap type (Time Series, Cross-Sectional, Sector, Correlation)
           - Choose color scale and display options
           - Configure additional parameters based on heatmap type
        
        4. **🔥 Generate**: Click the generate button to create your heatmap
        
        ### Heatmap Types:
        - **Time Series**: Shows how volatility changes over time for each asset
        - **Cross-Sectional**: Compares volatility across assets at specific time points
        - **Sector**: Aggregates individual stock volatilities into sector-level analysis
        - **Correlation**: Shows correlations between asset volatilities
        """)
    
    # Main heatmap analysis interface
    render_heatmap_analysis()
    
    # Additional information
    st.markdown("---")
    st.subheader("💡 Tips and Best Practices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #4ecdc4;">Parameter Selection</h4>
            <ul>
                <li><strong>Rolling Window:</strong> 20-30 days for short-term, 60-252 for longer-term analysis</li>
                <li><strong>Parkinson Method:</strong> More efficient for high-frequency data</li>
                <li><strong>Garman-Klass:</strong> Best for complete OHLC data availability</li>
                <li><strong>Historical:</strong> Traditional method, good baseline</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #45b7d1;">Interpretation Guide</h4>
            <ul>
                <li><strong>Red Colors:</strong> Higher volatility periods/assets</li>
                <li><strong>Blue/Green:</strong> Lower volatility periods/assets</li>
                <li><strong>Patterns:</strong> Look for clustering in time or across assets</li>
                <li><strong>Outliers:</strong> Extreme values may indicate market events</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    configure_streamlit()
    render_heatmap_page()
