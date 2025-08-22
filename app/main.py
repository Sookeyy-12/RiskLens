"""
RiskLens - Advanced Volatility Analysis Dashboard

A comprehensive Streamlit application for volatility heatmap analysis,
sector risk assessment, and quantitative finance visualization.
"""

import streamlit as st
import sys
import os

# Add src to path for importing our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import configure_streamlit
from pages.home import render_home_page
from pages.heatmap_analysis import render_heatmap_page
from pages.chart_analysis import render_chart_page


def main():
    """Main application entry point."""
    
    # Configure Streamlit
    configure_streamlit()
    
    # Sidebar navigation
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #ff6b6b; font-size: 2rem;">🔥 RiskLens</h1>
        <p style="color: #fafafa;">Volatility Analysis Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    page = st.sidebar.selectbox(
        "Navigate to:",
        [
            "🏠 Home",
            "🔥 Heatmap Analysis", 
            "📊 Chart Analysis"
        ],
        index=0
    )
    
    # Additional sidebar information
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div class="info-box">
        <h4 style="color: #4ecdc4;">Quick Navigation</h4>
        <ul>
            <li><strong>🏠 Home:</strong> Overview and getting started</li>
            <li><strong>🔥 Heatmaps:</strong> Interactive volatility visualizations</li>
            <li><strong>📊 Charts:</strong> Statistical analysis and comparisons</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Display help information
    with st.sidebar.expander("💡 Need Help?", expanded=False):
        st.markdown("""
        ### Quick Tips:
        - Start with predefined stock lists for quick analysis
        - Use 20-30 day windows for short-term volatility
        - Try different volatility methods to compare results
        - Sector analysis is great for portfolio insights
        
        ### Common Issues:
        - **No data**: Check ticker symbols and date ranges
        - **Slow loading**: Reduce number of tickers or date range
        - **Missing sectors**: Some tickers might not have sector data
        """)
    
    # Footer in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>RiskLens v1.0</p>
        <p>Built with Streamlit & Plotly</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if page == "🏠 Home":
        render_home_page()
    elif page == "🔥 Heatmap Analysis":
        render_heatmap_page()
    elif page == "📊 Chart Analysis":
        render_chart_page()


if __name__ == "__main__":
    main()