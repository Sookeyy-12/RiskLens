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
    import os
    
    # Get the absolute path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # Go up one level from src/
    data_dir = os.path.join(project_root, "data")
    csv_path = os.path.join(data_dir, "sector_mapping.csv")
    
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
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
        try:
            sector_df.to_csv(csv_path, index=False)
            print(f"Sector mapping saved to: {csv_path}")
        except Exception as e:
            print(f"Warning: Could not save sector mapping: {e}")
    
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

        # Handle single ticker case
        if len(tickers) == 1:
            ticker = tickers[0]
            
            # For single ticker, yfinance returns a simple DataFrame
            # We need to ensure it has the right structure
            if isinstance(data.columns, pd.MultiIndex):
                # If it's already MultiIndex, extract the ticker data
                df = data[ticker].copy() if ticker in data.columns.levels[0] else data.copy()
            else:
                # Simple DataFrame - this is the normal case for single ticker
                df = data.copy()
            
            # Add ticker column and create MultiIndex
            df = df.reset_index()  # Make Date a regular column
            df['Ticker'] = ticker
            df = df.set_index(['Date', 'Ticker'])
            
        else:
            # Multiple tickers case
            frames = []
            for ticker in tickers:
                try:
                    if isinstance(data.columns, pd.MultiIndex):
                        # Normal multi-ticker case
                        ticker_data = data[ticker].copy()
                    else:
                        # Edge case: single ticker in list but returned as simple DataFrame
                        ticker_data = data.copy()
                    
                    ticker_data = ticker_data.reset_index()
                    ticker_data['Ticker'] = ticker
                    ticker_data = ticker_data.set_index(['Date', 'Ticker'])
                    frames.append(ticker_data)
                except KeyError:
                    print(f"Warning: Could not find data for ticker {ticker}")
                    continue
            
            if frames:
                df = pd.concat(frames)
            else:
                raise ValueError("No valid data found for any of the provided tickers")

        return df
    else:
        raise NotImplementedError("Only yfinance provider is currently supported")
    
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

