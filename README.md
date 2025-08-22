# 🔥 RiskLens - Advanced Volatility Analysis Dashboard

A comprehensive Streamlit application for quantitative volatility analysis, featuring interactive heatmaps, sector risk assessment, and advanced statistical visualizations.

## ✨ Features

### 🔥 Interactive Volatility Heatmaps
- **Time Series Heatmaps**: Visualize how volatility changes over time
- **Cross-Sectional Heatmaps**: Compare volatility across assets at specific points
- **Sector Volatility Heatmaps**: Aggregate individual stocks into sector-level analysis
- **Correlation Heatmaps**: Analyze correlations between asset volatilities

### 📊 Multiple Volatility Models
- **Historical Volatility**: Traditional close-to-close returns method
- **Parkinson Estimator**: High-low range based, more efficient for intraday volatility
- **Garman-Klass Estimator**: OHLC-based estimator for comprehensive volatility capture
- **Beta-Adjusted Volatility**: Market-relative risk measures

### 🏭 Advanced Sector Analysis
- **Sector Risk Contribution**: Understand which sectors drive portfolio risk
- **Volatility Rankings**: Rank sectors and assets by volatility levels
- **Regime Detection**: Identify low, medium, and high volatility regimes
- **Correlation Analysis**: Sector-level correlation matrices

### 📈 Statistical Analysis Tools
- **Distribution Analysis**: Study volatility distributions and identify outliers
- **Method Comparison**: Side-by-side comparison of different volatility calculations
- **Time Series Analysis**: Trend analysis and pattern identification
- **Box Plots & Histograms**: Statistical visualization of volatility characteristics

### 👨‍💻 Developer Profile & Project Information
- **About Developer**: Comprehensive developer profile with skills and expertise
- **Project Showcase**: Detailed information about RiskLens features and capabilities
- **Technical Skills**: Overview of quantitative finance and development expertise
- **Social Connect**: Links to GitHub, LinkedIn, and other professional profiles
- **Roadmap**: Future development plans and feature enhancements

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Required packages (see `requirements_streamlit.txt`)

### Installation & Launch

#### Option 1: PowerShell (Windows - Recommended)
```powershell
# Navigate to the RiskLens directory
cd "C:\path\to\RiskLens"

# Run the PowerShell launcher
.\launch_app.ps1
```

#### Option 2: Python Launcher
```bash
# Navigate to the RiskLens directory
cd /path/to/RiskLens

# Run the Python launcher
python launch_app.py
```

#### Option 3: Direct Streamlit
```bash
# Install requirements
pip install -r requirements_streamlit.txt

# Launch directly
streamlit run app/main.py
```

## 🧭 Application Navigation

The RiskLens dashboard features an intuitive sidebar navigation with four main sections:
- **🏠 Home**: Welcome page with overview and getting started guide
- **🔥 Heatmap Analysis**: Interactive volatility heatmap generation and analysis
- **📊 Chart Analysis**: Statistical analysis, distribution plots, and method comparisons
- **👨‍💻 About Developer**: Developer profile, project information, and contact details

## 📊 Usage Guide

### 1. Home Page
- Overview of features and capabilities
- Navigation guide and quick start instructions
- Technical details about volatility methods

### 2. Heatmap Analysis
1. **Data Configuration**:
   - Choose from predefined stock lists (FAANG, S&P 500 Tech, Banking, etc.)
   - Or enter custom ticker symbols
   - Set analysis date range

2. **Volatility Parameters**:
   - Select volatility method (Historical, Parkinson, Garman-Klass)
   - Configure rolling window (5-252 days)
   - Option to annualize volatility values

3. **Visualization Settings**:
   - Choose heatmap type
   - Select color scale (RdYlBu_r, Viridis, Plasma, etc.)
   - Configure display options

4. **Generate & Analyze**:
   - Click "Generate Heatmap" to create interactive visualization
   - Explore summary statistics and insights

### 3. Chart Analysis
- **Volatility Comparison**: Compare different calculation methods
- **Sector Analysis**: Deep dive into sector-level volatility patterns
- **Distribution Analysis**: Statistical analysis of volatility distributions

### 4. About Developer
- **Developer Profile**: Meet the creator behind RiskLens
- **Technical Skills**: Overview of expertise in quantitative finance and development
- **Project Information**: Detailed insights into RiskLens development and features
- **Connect**: Social media links and contact information
- **Roadmap**: Future enhancements and development plans

## 🎨 Customization Options

### Color Schemes
- RdYlBu_r (Red-Yellow-Blue, recommended for volatility)
- Viridis (Perceptually uniform)
- Plasma (High contrast)
- Inferno (Heat-like)
- Spectral (Rainbow)

### Stock Lists
- **FAANG**: META, AAPL, AMZN, NFLX, GOOGL
- **S&P 500 Tech**: Major technology stocks
- **Banking**: Major financial institutions
- **Energy**: Oil & gas companies
- **Healthcare**: Pharmaceutical and biotech
- **Custom**: Enter your own ticker symbols

### Volatility Methods
- **Historical**: σ = √(252 × Var(log(Pt/Pt-1)))
- **Parkinson**: σ = √(1/(4ln2) × E[(ln(High/Low))²])
- **Garman-Klass**: Incorporates OHLC for improved efficiency

## 🔧 Technical Architecture

### Project Structure
```
RiskLens/
├── app/
│   ├── main.py              # Main Streamlit application
│   ├── config.py            # App configuration and styling
│   ├── components/
│   │   ├── heatmap.py       # Heatmap analysis components
│   │   └── charts.py        # Chart analysis components
│   └── pages/
│       ├── home.py          # Home page
│       ├── heatmap_analysis.py  # Volatility heatmap analysis
│       ├── chart_analysis.py    # Statistical chart analysis
│       └── about_developer.py   # Developer profile and project info
├── src/                     # Core RiskLens library
│   ├── data_fetcher.py      # Data acquisition functions
│   ├── volatility.py       # Volatility calculation methods
│   ├── sector_analysis.py  # Sector-level analysis
│   └── visualization.py    # Plotly visualization functions
├── launch_app.py            # Python launcher
├── launch_app.ps1           # PowerShell launcher
└── requirements_streamlit.txt
```

### Data Sources
- **Yahoo Finance (yfinance)**: Real-time and historical stock data
- **Company Fundamentals**: Sector classification
- **OHLCV Data**: Open, High, Low, Close, Volume for comprehensive analysis

### Performance Features
- **Caching**: Streamlit caching for data fetching (1-hour TTL)
- **Efficient Calculations**: Vectorized operations with NumPy/Pandas
- **Interactive Visualizations**: Plotly for responsive charts
- **Dark Theme**: Optimized for professional financial analysis

## 💡 Best Practices

### Parameter Selection
- **Short-term analysis**: 20-30 day rolling windows
- **Medium-term analysis**: 60-90 day windows
- **Long-term analysis**: 180-252 day windows
- **High-frequency data**: Parkinson or Garman-Klass methods
- **Limited data**: Historical volatility method

### Interpretation Guide
- **Red colors**: Higher volatility periods/assets (risk)
- **Blue/Green colors**: Lower volatility periods/assets (stability)
- **Clusters**: Look for patterns in time or across similar assets
- **Outliers**: Extreme values often indicate market events

### Common Use Cases
1. **Portfolio Risk Management**: Identify high-risk periods and assets
2. **Sector Rotation**: Use sector volatility for allocation decisions
3. **Risk Budgeting**: Understand sector contributions to portfolio risk
4. **Market Timing**: Identify volatility regime changes
5. **Stress Testing**: Analyze volatility during market stress periods

## 🛠️ Troubleshooting

### Common Issues
- **No data displayed**: Check ticker symbols and date ranges
- **Slow performance**: Reduce number of tickers or date range
- **Missing sector data**: Some tickers may not have sector classification
- **Import errors**: Ensure all requirements are installed

### Performance Tips
- Start with smaller date ranges for initial analysis
- Use predefined stock lists for faster loading
- Cache is cleared every hour - rerun for updated data
- Close browser tabs if memory usage is high

## 📈 Example Analysis Workflows

### Workflow 1: Market Stress Analysis
1. Select S&P 500 Tech stocks
2. Set date range covering recent market stress (e.g., 2022-2023)
3. Use Historical volatility with 30-day window
4. Generate Time Series Heatmap
5. Analyze patterns during stress periods

### Workflow 2: Sector Comparison
1. Choose diverse stock list (cross-sector)
2. Generate Sector Volatility Heatmap
3. Switch to Chart Analysis → Sector Analysis
4. Compare sector rankings and regime detection
5. Analyze correlation patterns

### Workflow 3: Method Validation
1. Select few stocks (3-5 tickers)
2. Use Chart Analysis → Volatility Comparison
3. Compare Historical, Parkinson, and Garman-Klass
4. Analyze differences in distribution and time series
5. Choose most appropriate method for your analysis

## 🎯 Future Enhancements

- Real-time data streaming
- Additional volatility models (EWMA, GARCH)
- Portfolio optimization integration
- Risk metrics (VaR, CVaR)
- Export functionality (PNG, PDF, Excel)
- API integration for automated analysis

## 📞 Support

For technical support, feature requests, or bug reports, please refer to the project documentation or create an issue in the repository.

---

**Built with ❤️ using Streamlit, Plotly, and the RiskLens quantitative finance library**
