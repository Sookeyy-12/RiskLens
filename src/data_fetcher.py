from typing import List, Tuple

import yfinance as yf
import pandas as pd

def get_ticker_list(index_name: str) -> List[str]:
    pass

def get_sector_mapping(tickers: List[str]) -> pd.DataFrame:
    pass

def fetch_ohlcv(
    tickers: List[str],
    start_date: str,
    end_date: str,
    provider: str = 'yfinance'
) -> pd.MultiIndex:
    """
    Fetches OHLCV data for tickers between start_date and end_date.
    Returns MultiIndex DataFrame: (Date, Ticker) with columns: Open, High, Low, Close, Adj Close, Volume
    """
    if provider == 'yfinance':
        data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', auto_adjust=False)

        # If single ticker, wrap it in a dict-like structure
        if len(tickers) == 1:
            ticker = tickers[0]
            df = data.copy()
            df['Ticker'] = ticker
            df = df.reset_index().set_index(['Date', 'Ticker'])
        else:
            frames = []
            for ticker in tickers:
                df = data[ticker].copy()
                df['Ticker'] = ticker
                df = df.reset_index().set_index(['Date', 'Ticker'])
                frames.append(df)
            df = pd.concat(frames)

        return df
    else:
        pass
    
def fetch_index_data(
    index_symbol: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Fetch Benchmark index OHLCV (for beta-adjusted volatility)
    """
    pass

