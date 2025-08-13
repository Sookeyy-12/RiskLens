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