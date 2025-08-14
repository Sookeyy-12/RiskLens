from typing import List, Tuple

import yfinance as yf
import pandas as pd

def get_ticker_list(index_name: str) -> List[str]:
    pass

def get_sector_mapping(tickers: List[str]) -> pd.DataFrame:
    """
    Get sector mapping for given tickers. First tries to load from CSV,
    if not available, fetches from yfinance and saves to CSV.
    """
    csv_path = "../data/sector_mapping.csv"
    
    try:
        # Try to load existing mapping
        sector_df = pd.read_csv(csv_path)
        
        # Check if all tickers are present
        missing_tickers = [t for t in tickers if t not in sector_df['Ticker'].values]
        
        if not missing_tickers:
            # Filter to only requested tickers
            return sector_df[sector_df['Ticker'].isin(tickers)]
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # File doesn't exist or is empty, start fresh
        sector_df = pd.DataFrame(columns=['Ticker', 'Sector'])
        missing_tickers = tickers
    
    # Fetch missing ticker info
    if missing_tickers:
        new_mappings = []
        for ticker in missing_tickers:
            try:
                info = yf.Ticker(ticker).info
                sector = info.get('sector', 'Unknown')
                new_mappings.append({'Ticker': ticker, 'Sector': sector})
            except Exception as e:
                print(f"Warning: Could not fetch sector for {ticker}: {e}")
                new_mappings.append({'Ticker': ticker, 'Sector': 'Unknown'})
        
        # Append new mappings
        new_df = pd.DataFrame(new_mappings)
        sector_df = pd.concat([sector_df, new_df], ignore_index=True)
        
        # Save updated mapping
        sector_df.to_csv(csv_path, index=False)
    
    # Return only requested tickers
    return sector_df[sector_df['Ticker'].isin(tickers)]

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
    data = yf.download(index_symbol, start=start_date, end=end_date, auto_adjust=False)
    data['Returns'] = data['Adj Close'].pct_change()
    return data

