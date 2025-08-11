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
    
def historical_volatiliy(
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

