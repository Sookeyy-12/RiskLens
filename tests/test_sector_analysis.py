#!/usr/bin/env python3
"""
Test script for sector_analysis.py implementations
"""

import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sector_analysis import (
    compute_sector_volatility,
    compute_sector_risk_contribution,
    compare_with_benchmark,
    rank_sectors_by_volatility,
    compute_sector_correlation,
    cluster_sectors_by_volatility,
    detect_sector_volatility_regimes
)

def create_sample_data():
    """Create sample data for testing"""
    # Create sample stock volatility data
    dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
    tickers = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'TSLA', 'META']
    
    # Generate realistic volatility data
    np.random.seed(42)
    data = {}
    base_vols = {'AAPL': 0.15, 'MSFT': 0.18, 'NVDA': 0.35, 'GOOGL': 0.20, 'TSLA': 0.45, 'META': 0.25}
    
    for ticker in tickers:
        # Add some randomness and trends
        vol_series = base_vols[ticker] + 0.1 * np.random.randn(len(dates)) + 0.05 * np.sin(np.arange(len(dates)) / 30)
        vol_series = np.maximum(vol_series, 0.05)  # Ensure positive volatility
        data[ticker] = vol_series
    
    stock_vol_df = pd.DataFrame(data, index=dates)
    
    # Create sector mapping
    sector_map = {
        'AAPL': 'Technology',
        'MSFT': 'Technology', 
        'NVDA': 'Technology',
        'GOOGL': 'Technology',
        'TSLA': 'Automotive',
        'META': 'Social Media'
    }
    
    # Create benchmark data
    benchmark_vol = 0.12 + 0.05 * np.random.randn(len(dates))
    benchmark_vol = np.maximum(benchmark_vol, 0.02)
    benchmark_series = pd.Series(benchmark_vol, index=dates)
    
    return stock_vol_df, sector_map, benchmark_series

def test_all_functions():
    """Test all sector analysis functions"""
    print("Creating sample data...")
    stock_vol_df, sector_map, benchmark_series = create_sample_data()
    
    print(f"Stock volatility data shape: {stock_vol_df.shape}")
    print(f"Sector mapping: {sector_map}")
    print(f"Date range: {stock_vol_df.index[0]} to {stock_vol_df.index[-1]}")
    print("-" * 50)
    
    # Test 1: Compute sector volatility
    print("1. Testing compute_sector_volatility...")
    try:
        sector_vol = compute_sector_volatility(stock_vol_df, sector_map, method="mean")
        print(f"   Result shape: {sector_vol.shape}")
        print(f"   Sectors: {list(sector_vol.columns)}")
        print(f"   Sample values:\n{sector_vol.head()}")
        print("   ✓ SUCCESS")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
    print()
    
    # Test 2: Compute risk contribution
    print("2. Testing compute_sector_risk_contribution...")
    try:
        risk_contrib = compute_sector_risk_contribution(stock_vol_df, sector_map)
        print(f"   Result shape: {risk_contrib.shape}")
        print(f"   Sample values:\n{risk_contrib.head()}")
        print("   ✓ SUCCESS")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
    print()
    
    # Test 3: Compare with benchmark
    print("3. Testing compare_with_benchmark...")
    try:
        sector_vol = compute_sector_volatility(stock_vol_df, sector_map)
        excess_vol = compare_with_benchmark(sector_vol, benchmark_series)
        print(f"   Result shape: {excess_vol.shape}")
        print(f"   Sample values:\n{excess_vol.head()}")
        print("   ✓ SUCCESS")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
    print()
    
    # Test 4: Rank sectors
    print("4. Testing rank_sectors_by_volatility...")
    try:
        sector_vol = compute_sector_volatility(stock_vol_df, sector_map)
        rankings = rank_sectors_by_volatility(sector_vol, top_n=3)
        print(f"   Rankings:\n{rankings}")
        print("   ✓ SUCCESS")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
    print()
    
    # Test 5: Compute correlation
    print("5. Testing compute_sector_correlation...")
    try:
        sector_vol = compute_sector_volatility(stock_vol_df, sector_map)
        corr_matrix = compute_sector_correlation(sector_vol)
        print(f"   Correlation matrix shape: {corr_matrix.shape}")
        print(f"   Sample correlations:\n{corr_matrix}")
        print("   ✓ SUCCESS")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
    print()
    
    # Test 6: Cluster sectors
    print("6. Testing cluster_sectors_by_volatility...")
    try:
        sector_vol = compute_sector_volatility(stock_vol_df, sector_map)
        
        # Test with simple distance-based clustering (fallback if sklearn not available)
        if len(sector_vol.columns) >= 2:
            clustering_result = cluster_sectors_by_volatility(sector_vol, method="hierarchical", n_clusters=2)
            print(f"   Clustering result keys: {list(clustering_result.keys())}")
            if 'cluster_labels' in clustering_result:
                print(f"   Cluster labels: {clustering_result['cluster_labels']}")
            elif 'error' in clustering_result:
                print(f"   Note: {clustering_result['error']}")
            print("   ✓ SUCCESS")
        else:
            print("   ⚠ SKIPPED: Not enough sectors for clustering")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
    print()
    
    # Test 7: Detect regimes
    print("7. Testing detect_sector_volatility_regimes...")
    try:
        sector_vol = compute_sector_volatility(stock_vol_df, sector_map)
        regimes = detect_sector_volatility_regimes(sector_vol, thresholds=(0.15, 0.30))
        print(f"   Regimes shape: {regimes.shape}")
        print(f"   Sample regimes:\n{regimes.head()}")
        
        # Count regime distribution
        print("\n   Regime distribution:")
        for sector in regimes.columns:
            regime_counts = regimes[sector].value_counts()
            print(f"     {sector}: {regime_counts.to_dict()}")
        print("   ✓ SUCCESS")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
    print()
    
    print("=" * 50)
    print("All tests completed!")

if __name__ == "__main__":
    test_all_functions()
