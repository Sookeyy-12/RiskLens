"""
RiskLens - A quantitative risk analysis package.

This package provides tools for fetching financial data, calculating volatility,
performing sector analysis, and various utility functions for risk analysis.
"""

# Import main modules
from . import data_fetcher
from . import sector_analysis
from . import utils
from . import volatility
from . import visualization

# Import key functions for direct access
from .data_fetcher import (
    get_ticker_list,
    get_sector_mapping,
    fetch_ohlcv,
    fetch_index_data
)

from .volatility import (
    compute_daily_returns,
    historical_volatility,
    parkinson_volatility,
    garman_klass_volatility,
    beta_adjusted_volatility,
    sector_volatility,
    volatility_summary,
    prepare_time_volatility_heatmap,
    prepare_cross_sectional_heatmap,
    prepare_sector_volatility_heatmap,
    prepare_correlation_heatmap
)

from .sector_analysis import (
    compute_sector_volatility,
    compute_sector_risk_contribution,
    compare_with_benchmark,
    rank_sectors_by_volatility,
    compute_sector_correlation,
    cluster_sectors_by_volatility,
    detect_sector_volatility_regimes
)

from .visualization import (
    create_volatility_heatmap,
    create_correlation_heatmap,
    create_time_series_plot,
    create_distribution_plot,
    create_box_plot,
    create_ranking_chart,
    create_regime_plot
)

__all__ = [
    # Modules
    'data_fetcher',
    'sector_analysis', 
    'utils',
    'volatility',
    'visualization',
    
    # Data fetching functions
    'get_ticker_list',
    'get_sector_mapping',
    'fetch_ohlcv',
    'fetch_index_data',
    
    # Volatility calculation functions
    'compute_daily_returns',
    'historical_volatility',
    'parkinson_volatility',
    'garman_klass_volatility',
    'beta_adjusted_volatility',
    'sector_volatility',
    'volatility_summary',
    'prepare_time_volatility_heatmap',
    'prepare_cross_sectional_heatmap',
    'prepare_sector_volatility_heatmap',
    'prepare_correlation_heatmap',
    
    # Sector analysis functions
    'compute_sector_volatility',
    'compute_sector_risk_contribution',
    'compare_with_benchmark',
    'rank_sectors_by_volatility',
    'compute_sector_correlation',
    'cluster_sectors_by_volatility',
    'detect_sector_volatility_regimes',
    
    # Visualization functions
    'create_volatility_heatmap',
    'create_correlation_heatmap',
    'create_time_series_plot',
    'create_distribution_plot',
    'create_box_plot',
    'create_ranking_chart',
    'create_regime_plot',
]