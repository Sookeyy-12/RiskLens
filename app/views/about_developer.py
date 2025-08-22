"""
About Developer Page - RiskLens Application

This page provides information about the developer and the project.
"""

import streamlit as st


def render_about_developer_page():
    """Render the About Developer page."""
    
    # Page header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #ff6b6b; font-size: 3rem;">👨‍💻 About Developer</h1>
        <p style="color: #888; font-size: 1.2rem;">Meet the creator behind RiskLens</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Developer information section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; padding: 2rem; text-align: center; 
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3); margin: 2rem 0;">            
        <h2 style="color: #fff; margin-bottom: 0.5rem;">Sookeyy-12</h2>
            <p style="color: #e0e0e0; font-style: italic; margin-bottom: 1rem;">
                Quantitative Finance Enthusiast & Developer
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # About section
    st.markdown("## 🎯 About Me")
    st.markdown("""
    I'm a passionate developer and quantitative finance enthusiast who believes in the power of 
    data-driven decision making in financial markets. With expertise in Python, data analysis, 
    and financial modeling, I created RiskLens to democratize advanced volatility analysis tools.
    
    
    """)
    st.info(
        "🔗 **Know more about me on my portfolio:** [suketkamboj.tech](https://suketkamboj.tech)",
        icon="🌐"
    )
    # Project information
    st.markdown("## 🔥 About RiskLens")
    st.markdown("""
    RiskLens is a comprehensive volatility analysis dashboard designed for traders, 
    analysts, and finance professionals. The application provides:
    
    - **Interactive Heatmaps**: Visualize volatility patterns across multiple assets
    - **Sector Analysis**: Understand risk distribution across different market sectors
    - **Statistical Tools**: Advanced metrics and comparison capabilities
    - **Real-time Data**: Integration with financial data providers
    - **Modern UI**: Clean, intuitive interface built with Streamlit
    """)
    
    # Features showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 10px; padding: 1.5rem; text-align: center; height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h4 style="color: #333;">Interactive Charts</h4>
            <p style="color: #666; font-size: 0.9rem;">Dynamic visualizations with Plotly</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 10px; padding: 1.5rem; text-align: center; height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <h4 style="color: #333;">Real-time Data</h4>
            <p style="color: #666; font-size: 0.9rem;">Live market data integration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 10px; padding: 1.5rem; text-align: center; height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h4 style="color: #333;">Advanced Analytics</h4>
            <p style="color: #666; font-size: 0.9rem;">Professional-grade analysis tools</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Connect section
    st.markdown("## 🌐 Connect With Me")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://github.com/Sookeyy-12" target="_blank" style="text-decoration: none;">
                <div style="background: #333; color: white; border-radius: 10px; padding: 1rem; margin: 0.5rem;">
                    <div style="font-size: 2rem;">🐙</div>
                    <div style="font-size: 0.8rem;">GitHub</div>
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://linkedin.com/in/suket-kamboj-212416255" target="_blank" style="text-decoration: none;">
                <div style="background: #0077b5; color: white; border-radius: 10px; padding: 1rem; margin: 0.5rem;">
                    <div style="font-size: 2rem;">💼</div>
                    <div style="font-size: 0.8rem;">LinkedIn</div>
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <a href="mailto:suket.kamboj12@example.com" style="text-decoration: none;">
                <div style="background: #ea4335; color: white; border-radius: 10px; padding: 1rem; margin: 0.5rem;">
                    <div style="font-size: 2rem;">📧</div>
                    <div style="font-size: 0.8rem;">Email</div>
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://x.com/SookeyyK" target="_blank" style="text-decoration: none;">
                <div style="background: #1da1f2; color: white; border-radius: 10px; padding: 1rem; margin: 0.5rem;">
                    <div style="font-size: 2rem;">
                    X</div>
                    <div style="font-size: 0.8rem;">X</div>
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://suketkamboj.tech" target="_blank" style="text-decoration: none;">
                <div style="background: #ff6b6b; color: white; border-radius: 10px; padding: 1rem; margin: 0.5rem;">
                    <div style="font-size: 2rem;">🌐</div>
                    <div style="font-size: 0.8rem;">Portfolio</div>
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # Project statistics or achievements
    st.markdown("## 📈 Project Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Lines of Code", "2,500+", "Growing")
    
    with col2:
        st.metric("Features", "15+", "Active")
    
    with col3:
        st.metric("Data Sources", "Multiple", "Integrated")
    
    with col4:
        st.metric("Version", "1.0", "Stable")
    
    # Future plans
    st.markdown("## 🚀 Future Plans")
    st.markdown("""
    I'm continuously working to improve RiskLens and add new features:
    
    - 🔮 **Machine Learning Models**: Predictive volatility forecasting
    - 📱 **Mobile App**: React Native companion app
    - 🔄 **API Integration**: RESTful API for external integrations
    - 📊 **Advanced Metrics**: More sophisticated risk measures
    - 🎨 **UI Enhancements**: Even more intuitive user experience
    - 🌍 **Multi-Market Support**: Global market coverage
    """)
    
    # Thank you message
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; color: white;">
        <h3>Thank You for Using RiskLens! 🙏</h3>
        <p>Your feedback and suggestions are always welcome. Let's build better financial tools together!</p>
    </div>
    """, unsafe_allow_html=True)
