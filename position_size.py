# portfolio_size.py

from asset_data import AssetData
from typing import List, Optional

def set_position_size(
    asset: AssetData,
    drift_threshold: float = 0.05,
    drift_pct_threshold: float = 0.50
) -> None:
    """
    Calculates and sets drift, drift_pct, and position_size on an AssetData object.
    """
    if (
        asset.weight is None or
        asset.target is None or
        asset.target == 0
    ):
        asset.drift = None
        asset.drift_pct = None
        asset.position_size = "-"
        return

    # Calculate drift and drift %
    asset.drift = asset.weight - asset.target
    asset.drift_pct = asset.drift / asset.target

    # Classify position
    if asset.drift > drift_threshold or asset.drift_pct > drift_pct_threshold:
        asset.position_size = "oversize"
    elif asset.drift < -drift_threshold or asset.drift_pct < -drift_pct_threshold:
        asset.position_size = "undersize"
    else:
        asset.position_size = "-"

def assign_position_sizes(assets: List[AssetData]) -> List[AssetData]:
    """
    Applies set_position_size to all assets in the portfolio.
    """
    for asset in assets:
        set_position_size(asset)
    return assets
