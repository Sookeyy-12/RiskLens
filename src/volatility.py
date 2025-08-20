import pandas as pd
import numpy as np

def compute_daily_returns(
    df: pd.DataFrame,
    use_log: bool = False
) -> pd.DataFrame:
    """
    Compute daily returns from adjusted close prices.
    Args:
        df: DataFrame with MultiIndex (Date, Ticker) or columns ['Date', 'Ticker', 'Adj Close']
        use_log: Whether to compute log returns instead of simple pct change.
    Returns:
        DataFrame with 'Returns' column.
    """
    if use_log:
        returns = np.log(df['Adj Close'] / df['Adj Close'].shift(1))
        return returns
    else:
        returns = df['Adj Close'].pct_change()
        return returns
    
def historical_volatility(
    df: pd.DataFrame,
    window: int = 30,
    annualize: bool = True
) -> pd.DataFrame:
    """
    Compute rolling historical volatility over given window
    """
    returns = compute_daily_returns(df)
    volatility = returns.rolling(window=window).std()
    if annualize:
        volatility *= np.sqrt(252)
    return volatility

def parkinson_volatility(
    df: pd.DataFrame,
    window: int = 30,
    annualize: bool = True
) -> pd.DataFrame:
    """
    Compute Parkinson volatility using high low prices.
    Formula: sqrt(1/(4ln2) * mean((ln(High/Low))^2)) × √annualization
    """
    ln_high_low = np.log(df['High'] / df['Low'])
    park_vol = np.sqrt(1 / (4 * np.log(2)) * ln_high_low.rolling(window=window).mean())
    if annualize:
        park_vol *= np.sqrt(252)
    return park_vol

def garman_klass_volatility(
    df : pd.DataFrame,
    window: int = 30,
    annualize: bool = True
) -> pd.DataFrame:
    """
    Computes Garman-Klass volatility using OHLC data
    """
    gk = np.sqrt(
        0.5 * np.power(np.log(df['High'] / df['Low']), 2) -
        (2 * np.log(2) - 1) * np.power(np.log(df['Close'] / df['Open']), 2)
    )
    if annualize:
        gk *= np.sqrt(252)
    return gk

def beta_adjusted_volatility(
    stock_vol_df: pd.DataFrame,
    benchmark_returns: pd.Series,
) -> pd.DataFrame:
    """
    Adjust Volatility by removing market (benchmark) risk.
    """
    cov_matrix = np.cov(stock_vol_df['Returns'], benchmark_returns)
    beta = cov_matrix[0, 1] / cov_matrix[1, 1]
    stock_vol_df['Adjusted Volatility'] = stock_vol_df['Volatility'] - beta * (benchmark_returns.std() - stock_vol_df['Volatility'])
    return stock_vol_df

def sector_volatility(
    vol_df: pd.DataFrame,
    sector_mapping: pd.DataFrame
) -> pd.DataFrame:
    """
    Aggregates volatility values by sector for heatmap visualization
    """
    vol_df = vol_df.join(sector_mapping.set_index('Ticker'), on='Ticker')
    sector_vol = vol_df.groupby('Sector')['Volatility'].mean()
    return sector_vol

def volatility_summary(
    df: pd.DataFrame,
    benchmark_df: pd.DataFrame,
    sector_map: pd.DataFrame,
    window: int = 30,
) -> pd.DataFrame:
    """
    One-Stop API to compute:
        - Daily Returns
        - Historical Volatility
        - Parkinson Volatility
        - Sector Average Volatility
        - Beta-Adjusted Volatility
    Returns DataFrame ready for heatmap plotting
    """
    daily_returns = compute_daily_returns(df)
    historical_vol = historical_volatility(df, window=window)
    parkinson_vol = parkinson_volatility(df, window=window)
    sector_vol = sector_volatility(historical_vol, sector_map)
    beta_adj_vol = beta_adjusted_volatility(historical_vol, benchmark_df['Returns'])

    summary_df = pd.DataFrame({
        'Daily Returns': daily_returns,
        'Historical Volatility': historical_vol,
        'Parkinson Volatility': parkinson_vol,
        'Sector Average Volatility': sector_vol,
        'Beta-Adjusted Volatility': beta_adj_vol
    })

    return summary_df

def prepare_time_volatility_heatmap(
    df: pd.DataFrame,
    window: int = 30,
    freq: str = 'M'  # 'D', 'W', 'M', 'Q' for daily, weekly, monthly, quarterly
) -> pd.DataFrame:
    """
    Prepare volatility data for time-based heatmap.
    X-axis: Time periods (dates)
    Y-axis: Tickers/Assets
    Values: Volatility measures
    """
    vol_data = historical_volatility(df, window=window)
    
    # Reshape for heatmap: index=dates, columns=tickers
    if hasattr(vol_data.index, 'levels'):  # MultiIndex
        # Unstack to get tickers as columns, dates as index
        vol_pivot = vol_data.unstack(level=1)  # Assuming ticker is level 1
        
        # Ensure index is DatetimeIndex for resampling
        if not isinstance(vol_pivot.index, pd.DatetimeIndex):
            # If index is not datetime, try to convert
            vol_pivot.index = pd.to_datetime(vol_pivot.index)
    else:
        # Single series - convert to DataFrame
        vol_pivot = vol_data.to_frame('Volatility')
        if not isinstance(vol_pivot.index, pd.DatetimeIndex):
            vol_pivot.index = pd.to_datetime(vol_pivot.index)
    
    # Resample to desired frequency
    if freq != 'D':
        vol_pivot = vol_pivot.resample(freq).last()
    
    return vol_pivot

def prepare_cross_sectional_heatmap(
    df: pd.DataFrame,
    benchmark_df: pd.DataFrame = None,
    window: int = 30
) -> pd.DataFrame:
    """
    Prepare cross-sectional volatility comparison heatmap.
    X-axis: Different volatility measures
    Y-axis: Tickers/Assets
    Values: Volatility values
    """
    tickers = df.index.get_level_values(1).unique() if hasattr(df.index, 'levels') else ['Asset']
    
    results = []
    for ticker in tickers:
        ticker_data = df.xs(ticker, level=1) if hasattr(df.index, 'levels') else df
        
        hist_vol = historical_volatility(ticker_data, window=window).dropna().iloc[-1]
        park_vol = parkinson_volatility(ticker_data, window=window).dropna().iloc[-1]
        gk_vol = garman_klass_volatility(ticker_data, window=window).dropna().iloc[-1]
        
        row_data = {
            'Historical Vol': hist_vol,
            'Parkinson Vol': park_vol,
            'Garman-Klass Vol': gk_vol
        }
        
        # Add beta-adjusted if benchmark provided
        if benchmark_df is not None:
            try:
                returns = compute_daily_returns(ticker_data).dropna()
                
                # Handle benchmark data structure properly
                if hasattr(benchmark_df.index, 'levels'):
                    # If benchmark has MultiIndex, take the first ticker/level
                    benchmark_series = benchmark_df.iloc[:, 0] if len(benchmark_df.columns) > 0 else benchmark_df['Adj Close']
                    bench_returns = compute_daily_returns(pd.DataFrame({'Adj Close': benchmark_series})).dropna()
                else:
                    # Simple DataFrame structure
                    bench_returns = compute_daily_returns(benchmark_df).dropna()
                
                # Align the series - ensure both are Series, not DataFrames
                if isinstance(returns, pd.DataFrame):
                    returns = returns.iloc[:, 0]  # Take first column if DataFrame
                if isinstance(bench_returns, pd.DataFrame):
                    bench_returns = bench_returns.iloc[:, 0]  # Take first column if DataFrame
                
                # Align on common dates
                aligned_returns, aligned_bench = returns.align(bench_returns, join='inner')
                
                if len(aligned_returns) > 10:  # Need sufficient data points
                    # Calculate correlation coefficient
                    correlation = np.corrcoef(aligned_returns.values, aligned_bench.values)[0, 1]
                    
                    # Beta-adjusted volatility (simplified approach)
                    if not np.isnan(correlation):
                        row_data['Beta-Adj Vol'] = hist_vol * (1 - abs(correlation) * 0.3)
                    else:
                        row_data['Beta-Adj Vol'] = hist_vol
                else:
                    row_data['Beta-Adj Vol'] = hist_vol  # Fallback to historical vol
            except Exception as e:
                print(f"Warning: Could not calculate beta for {ticker}: {str(e)[:100]}...")
                row_data['Beta-Adj Vol'] = hist_vol  # Fallback to historical vol
        
        results.append(pd.Series(row_data, name=ticker))
    
    return pd.DataFrame(results)

def prepare_sector_volatility_heatmap(
    df: pd.DataFrame,
    sector_mapping: pd.DataFrame,
    window: int = 30
) -> pd.DataFrame:
    """
    Prepare sector-based volatility heatmap.
    X-axis: Volatility measures
    Y-axis: Sectors
    Values: Average volatility by sector
    """
    tickers = df.index.get_level_values(1).unique() if hasattr(df.index, 'levels') else sector_mapping['Ticker'].values
    
    sector_results = {}
    
    for sector in sector_mapping['Sector'].unique():
        sector_tickers = sector_mapping[sector_mapping['Sector'] == sector]['Ticker'].values
        sector_vols = []
        
        for ticker in sector_tickers:
            if ticker in tickers:
                ticker_data = df.xs(ticker, level=1) if hasattr(df.index, 'levels') else df
                
                hist_vol = historical_volatility(ticker_data, window=window).dropna().iloc[-1]
                park_vol = parkinson_volatility(ticker_data, window=window).dropna().iloc[-1]
                gk_vol = garman_klass_volatility(ticker_data, window=window).dropna().iloc[-1]
                
                sector_vols.append({
                    'Historical Vol': hist_vol,
                    'Parkinson Vol': park_vol,
                    'Garman-Klass Vol': gk_vol
                })
        
        if sector_vols:
            avg_vols = pd.DataFrame(sector_vols).mean()
            sector_results[sector] = avg_vols
    
    return pd.DataFrame(sector_results).T

def prepare_correlation_heatmap(
    df: pd.DataFrame,
    window: int = 30
) -> pd.DataFrame:
    """
    Prepare volatility correlation heatmap.
    X-axis: Tickers/Assets
    Y-axis: Tickers/Assets  
    Values: Volatility correlation coefficients
    """
    vol_data = {}
    tickers = df.index.get_level_values(1).unique() if hasattr(df.index, 'levels') else ['Asset']
    
    for ticker in tickers:
        ticker_data = df.xs(ticker, level=1) if hasattr(df.index, 'levels') else df
        vol_data[ticker] = historical_volatility(ticker_data, window=window).dropna()
    
    vol_df = pd.DataFrame(vol_data)
    correlation_matrix = vol_df.corr()
    
    return correlation_matrix