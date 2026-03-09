# price_signal.py
from typing import List
from asset_data import AssetData


def assign_price_signal(assets: List[AssetData]) -> List[AssetData]:
    """
    Generate price signals based on:
    - drawdown from 52w high
    - rebound from 52w low
    - rebound from multi-year low
    """

    for asset in assets:

        # Only evaluate investment assets
        if asset.asset_class not in {"Core", "Growth", "Speculative"}:
            asset.price_signal = None
            continue

        if (
            asset.price is None
            or asset.high_52w is None
            or asset.low_52w is None
            or asset.mdd is None
            or asset.cagr is None
            or asset.rebound is None
        ):
            asset.price_signal = None
            continue

        # --- Calculate price moves ---
        asset.drop_52w = (asset.price - asset.high_52w) / asset.high_52w
        asset.gain_52w = (asset.price - asset.low_52w) / asset.low_52w

        if asset.low_years:
            asset.gain_years = (asset.price - asset.low_years) / asset.low_years
        else:
            asset.gain_years = None

        # --- Thresholds ---
        mdd_threshold = -asset.mdd
        rebound_threshold = asset.rebound

        # --- Signal classification ---
        if asset.drop_52w <= mdd_threshold:
            asset.price_signal = "oversold"

        elif (
            asset.gain_52w >= asset.cagr
            or (asset.gain_years is not None and asset.gain_years >= rebound_threshold)
        ):
            asset.price_signal = "overbought"

        else:
            asset.price_signal = "-"

    return assets
