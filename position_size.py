# position_size.py
from asset_data import AssetData
from typing import Optional

def set_position_size(
    asset: AssetData,
    drift_threshold: float = 0.05,
    drift_pct_threshold: float = 0.50
) -> None:
    """
    Calculates and sets drift, drift_pct, and position_size on an AssetData object.
    Skips calculation entirely if asset_type is missing.
    """

    # If asset_type is not defined, skip position size logic
    if asset.asset_type is None:
        asset.drift = None
        asset.drift_pct = None
        asset.position_size = "-"
        return

    # If target is zero and weight is known, classify as oversize
    if asset.target == 0 and asset.weight is not None:
        asset.drift = asset.weight
        asset.drift_pct = None
        asset.position_size = "oversize"
        return

    # Skip if essential values are missing
    if asset.weight is None or asset.target is None:
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
