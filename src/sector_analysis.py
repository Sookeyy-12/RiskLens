import pandas as pd
import numpy as np
from typing import Dict, Union, Optional, Tuple, Any

# Optional imports for clustering functionality
try:
    from sklearn.cluster import KMeans, AgglomerativeClustering
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
    from scipy.spatial.distance import pdist, squareform
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

def compute_sector_volatility(stock_vol_df: pd.DataFrame, sector_map: Dict[str, str], method: str = "mean") -> pd.DataFrame:
    """
    Aggregate stock-level volatility into sector-level volatility.
    
    Args:
        stock_vol_df (pd.DataFrame): Stock volatilities, cols=tickers, rows=dates.
        sector_map (dict): {ticker: sector}.
        method (str): "mean" (default), "median", or "weighted".
    
    Returns:
        pd.DataFrame: Sector-level volatility (sectors × dates).
    """
    if stock_vol_df.empty:
        return pd.DataFrame()
    
    # Create a mapping DataFrame for joining
    sector_df = pd.DataFrame(list(sector_map.items()), columns=['Ticker', 'Sector'])
    
    # Filter stock_vol_df to only include tickers in sector_map
    available_tickers = [col for col in stock_vol_df.columns if col in sector_map]
    filtered_vol_df = stock_vol_df[available_tickers].copy()
    
    # Transpose to have tickers as rows for easier processing
    vol_transposed = filtered_vol_df.T
    vol_transposed.index.name = 'Ticker'
    vol_transposed = vol_transposed.reset_index()
    
    # Merge with sector mapping
    vol_with_sectors = vol_transposed.merge(sector_df, on='Ticker', how='left')
    
    # Group by sector and aggregate
    vol_cols = [col for col in vol_with_sectors.columns if col not in ['Ticker', 'Sector']]
    
    if method == "mean":
        sector_vol = vol_with_sectors.groupby('Sector')[vol_cols].mean()
    elif method == "median":
        sector_vol = vol_with_sectors.groupby('Sector')[vol_cols].median()
    elif method == "weighted":
        # Equal weighting for now - can be enhanced with market cap weighting
        sector_vol = vol_with_sectors.groupby('Sector')[vol_cols].mean()
    else:
        raise ValueError(f"Method '{method}' not supported. Use 'mean', 'median', or 'weighted'.")
    
    return sector_vol.T

def compute_sector_risk_contribution(stock_vol_df: pd.DataFrame, sector_map: Dict[str, str], weights: Optional[Union[Dict, pd.Series]] = None) -> pd.DataFrame:
    """
    Compute each sector's contribution to total market volatility.
    
    Args:
        stock_vol_df (pd.DataFrame): Stock volatilities.
        sector_map (dict): {ticker: sector}.
        weights (dict or pd.Series): Portfolio weights, default equal.
    
    Returns:
        pd.DataFrame: Sector risk contribution (% of total).
    """
    if stock_vol_df.empty:
        return pd.DataFrame()
    
    # Get sector volatilities
    sector_vol_df = compute_sector_volatility(stock_vol_df, sector_map, method="mean")
    
    # Setup weights
    if weights is None:
        # Equal weights for all sectors
        sectors = list(set(sector_map.values()))
        weights = pd.Series(1.0/len(sectors), index=sectors)
    elif isinstance(weights, dict):
        weights = pd.Series(weights)
    
    # Normalize weights to sum to 1
    weights = weights / weights.sum()
    
    # Calculate weighted sector volatilities
    risk_contributions = []
    for date in sector_vol_df.index:
        date_vols = sector_vol_df.loc[date]
        
        # Filter weights to match available sectors
        available_sectors = date_vols.dropna().index
        date_weights = weights.reindex(available_sectors).fillna(0)
        date_weights = date_weights / date_weights.sum() if date_weights.sum() > 0 else date_weights
        
        # Calculate portfolio variance (simplified approach)
        weighted_vols = date_vols * date_weights
        
        # Risk contribution = weight * volatility / total_weighted_volatility
        total_weighted_vol = weighted_vols.sum()
        if total_weighted_vol > 0:
            risk_contrib = (weighted_vols / total_weighted_vol) * 100  # Convert to percentage
        else:
            risk_contrib = pd.Series(0, index=available_sectors)
        
        risk_contributions.append(risk_contrib)
    
    risk_contrib_df = pd.concat(risk_contributions, axis=1, keys=sector_vol_df.index).T
    return risk_contrib_df

def compare_with_benchmark(sector_vol_df: pd.DataFrame, benchmark_vol_series: pd.Series) -> pd.DataFrame:
    """
    Compare sector volatilities with a benchmark (e.g. SPY/NIFTY).
    
    Args:
        sector_vol_df (pd.DataFrame): Sector volatilities over time.
        benchmark_vol_series (pd.Series): Benchmark volatility time series.
    
    Returns:
        pd.DataFrame: Excess volatility (sector_vol - benchmark_vol).
    """
    if sector_vol_df.empty or benchmark_vol_series.empty:
        return pd.DataFrame()
    
    # Align dates between sector volatilities and benchmark
    common_dates = sector_vol_df.index.intersection(benchmark_vol_series.index)
    
    if len(common_dates) == 0:
        print("Warning: No common dates between sector volatilities and benchmark")
        return pd.DataFrame()
    
    # Calculate excess volatility
    excess_vol = sector_vol_df.loc[common_dates].copy()
    benchmark_aligned = benchmark_vol_series.loc[common_dates]
    
    for sector in excess_vol.columns:
        excess_vol[sector] = excess_vol[sector] - benchmark_aligned
    
    return excess_vol

def rank_sectors_by_volatility(sector_vol_df: pd.DataFrame, date: Optional[str] = None, top_n: Optional[int] = None) -> Union[pd.Series, pd.DataFrame]:
    """
    Rank sectors by volatility for a given date or across time.
    
    Args:
        sector_vol_df (pd.DataFrame): Sector volatilities over time.
        date (str, optional): Specific date to rank. If None, ranks across all time.
        top_n (int, optional): Number of top sectors to return.
    
    Returns:
        pd.Series or pd.DataFrame: Rankings.
    """
    if sector_vol_df.empty:
        return pd.Series()
    
    if date is not None:
        # Rank for specific date
        if date in sector_vol_df.index:
            date_vols = sector_vol_df.loc[date].dropna()
            ranked = date_vols.sort_values(ascending=False)
            
            if top_n is not None:
                ranked = ranked.head(top_n)
                
            return ranked
        else:
            print(f"Warning: Date {date} not found in data")
            return pd.Series()
    else:
        # Rank across all time (using mean volatility)
        mean_vols = sector_vol_df.mean().dropna()
        ranked = mean_vols.sort_values(ascending=False)
        
        if top_n is not None:
            ranked = ranked.head(top_n)
            
        # Create a DataFrame with rankings
        ranking_df = pd.DataFrame({
            'Sector': ranked.index,
            'Average_Volatility': ranked.values,
            'Rank': range(1, len(ranked) + 1)
        })
        
        return ranking_df

def compute_sector_correlation(sector_vol_df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """
    Compute correlation between sector volatility time series.
    
    Args:
        sector_vol_df (pd.DataFrame): Sector volatilities over time.
        method (str): Correlation method - "pearson", "spearman", or "kendall".
    
    Returns:
        pd.DataFrame: Correlation matrix.
    """
    if sector_vol_df.empty:
        return pd.DataFrame()
    
    # Remove columns with all NaN values
    cleaned_df = sector_vol_df.dropna(axis=1, how='all')
    
    if cleaned_df.empty:
        return pd.DataFrame()
    
    # Calculate correlation matrix
    corr_matrix = cleaned_df.corr(method=method)
    
    return corr_matrix

def cluster_sectors_by_volatility(sector_vol_df: pd.DataFrame, method: str = "hierarchical", n_clusters: int = 3) -> Dict[str, Any]:
    """
    Cluster sectors based on volatility patterns.
    
    Args:
        sector_vol_df (pd.DataFrame): Sector volatilities over time.
        method (str): Clustering method - "hierarchical" or "kmeans".
        n_clusters (int): Number of clusters for k-means.
    
    Returns:
        dict: Dictionary containing cluster labels and additional information.
    """
    if sector_vol_df.empty:
        return {}
    
    # Check for required dependencies
    if method == "hierarchical" and not SCIPY_AVAILABLE:
        return {"error": "scipy is required for hierarchical clustering. Please install with: pip install scipy"}
    
    if method == "kmeans" and not SKLEARN_AVAILABLE:
        return {"error": "scikit-learn is required for k-means clustering. Please install with: pip install scikit-learn"}
    
    # Prepare data - transpose so sectors are rows
    data = sector_vol_df.T.dropna()
    
    if data.empty or len(data) < 2:
        return {"error": "Insufficient data for clustering"}
    
    result = {"sectors": data.index.tolist()}
    
    if method == "hierarchical":
        # Hierarchical clustering
        if len(data) > 1:
            # Calculate distance matrix
            distances = pdist(data, metric='euclidean')
            linkage_matrix = linkage(distances, method='ward')
            
            # Get cluster labels
            cluster_labels = fcluster(linkage_matrix, n_clusters, criterion='maxclust')
            
            result.update({
                "method": "hierarchical",
                "cluster_labels": dict(zip(data.index, cluster_labels)),
                "linkage_matrix": linkage_matrix,
                "n_clusters": n_clusters
            })
        
    elif method == "kmeans":
        # K-means clustering
        if len(data) >= n_clusters:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(data)
            
            result.update({
                "method": "kmeans",
                "cluster_labels": dict(zip(data.index, cluster_labels + 1)),  # +1 to start from 1
                "cluster_centers": kmeans.cluster_centers_,
                "inertia": kmeans.inertia_,
                "n_clusters": n_clusters
            })
        else:
            result["error"] = f"Number of sectors ({len(data)}) is less than n_clusters ({n_clusters})"
    
    else:
        result["error"] = f"Method '{method}' not supported. Use 'hierarchical' or 'kmeans'."
    
    return result

def detect_sector_volatility_regimes(sector_vol_df: pd.DataFrame, thresholds: Tuple[float, float] = (0.15, 0.30)) -> pd.DataFrame:
    """
    Classify volatility regimes (low/medium/high) for each sector.
    
    Args:
        sector_vol_df (pd.DataFrame): Sector volatilities over time.
        thresholds (tuple): (low_threshold, high_threshold).
    
    Returns:
        pd.DataFrame: Regime labels per sector over time.
    """
    if sector_vol_df.empty:
        return pd.DataFrame()
    
    low_threshold, high_threshold = thresholds
    
    # Create regime classification
    regime_df = sector_vol_df.copy()
    
    for sector in regime_df.columns:
        sector_data = regime_df[sector]
        
        # Classify regimes
        regime_df[sector] = pd.cut(
            sector_data,
            bins=[-np.inf, low_threshold, high_threshold, np.inf],
            labels=['Low', 'Medium', 'High'],
            include_lowest=True
        )
    
    return regime_df


