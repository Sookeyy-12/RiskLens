#!/usr/bin/env python3
"""
Test script for sector mapping functionality.
"""

import sys
import os

# Add src to path
sys.path.append('.')

def test_sector_mapping():
    """Test the sector mapping function."""
    try:
        from src.data_fetcher import get_sector_mapping
        print("✅ Import successful")
        
        # Test with a single ticker
        print("🔍 Testing with AAPL...")
        result = get_sector_mapping(['AAPL'])
        
        print(f"📊 Result shape: {result.shape}")
        print(f"📋 Columns: {result.columns.tolist()}")
        print(f"📈 Data:")
        print(result)
        
        if not result.empty:
            print("✅ Sector mapping test successful!")
            return True
        else:
            print("❌ No data returned")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_sector_mapping()
