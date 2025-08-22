#!/usr/bin/env python3
"""
Test script for updated data fetcher with single ticker.
"""

import sys
import os

# Add src to path
sys.path.append('.')

def test_data_fetcher():
    """Test the updated data fetcher function."""
    try:
        from src.data_fetcher import fetch_ohlcv
        
        print("🔍 Testing updated data fetcher...")
        
        # Test single ticker
        print("\n--- Single Ticker Test ---")
        tickers = ['AAPL']
        data = fetch_ohlcv(tickers, '2023-01-01', '2023-06-01')
        
        print(f"Data shape: {data.shape}")
        print(f"Index levels: {data.index.names}")
        print(f"Columns: {data.columns.tolist()}")
        print(f"Index values sample: {data.index.get_level_values('Ticker').unique()}")
        
        # Test data extraction
        ticker_data = data.xs('AAPL', level='Ticker')
        print(f"Extracted data shape: {ticker_data.shape}")
        print(f"Extracted columns: {ticker_data.columns.tolist()}")
        print(f"Has Adj Close: {'Adj Close' in ticker_data.columns}")
        
        if 'Adj Close' in ticker_data.columns:
            print("✅ Single ticker test successful!")
        else:
            print("❌ Missing Adj Close column")
            
        # Test multiple tickers
        print("\n--- Multiple Ticker Test ---")
        tickers = ['AAPL', 'GOOGL']
        data_multi = fetch_ohlcv(tickers, '2023-01-01', '2023-06-01')
        
        print(f"Multi data shape: {data_multi.shape}")
        print(f"Multi index levels: {data_multi.index.names}")
        print(f"Multi columns: {data_multi.columns.tolist()}")
        print(f"Multi tickers: {data_multi.index.get_level_values('Ticker').unique()}")
        
        # Test extraction for each ticker
        for ticker in tickers:
            ticker_data = data_multi.xs(ticker, level='Ticker')
            print(f"{ticker} - shape: {ticker_data.shape}, has Adj Close: {'Adj Close' in ticker_data.columns}")
        
        print("✅ All tests successful!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_data_fetcher()
