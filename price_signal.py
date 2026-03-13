# price_signal.py
from typing import List
from asset_data import AssetData


def assign_price_signals(assets: List[AssetData], years_rebound: int) -> List[AssetData]:
    """
    Generate price signals based on:
    - drawdown from 52w high
    - rebound from 52w low
    - rebound from multi-year low

    Also calculate:
    - gain_years
    - realized CAGR from gain_years
    - calmar_ratio = realized CAGR / |MDD|
    """

    for asset in assets:

        # Only evaluate investment assets
        if asset.asset_class not in {"Core", "Growth", "Speculative"}:
            asset.price_signal = None
            asset.calmar_ratio = None
            asset.gain_years = None
            asset.drop_52w = None
            asset.gain_52w = None
            continue

        # Reset derived fields
        asset.price_signal = None
        asset.calmar_ratio = None
        asset.gain_years = None
        asset.drop_52w = None
        asset.gain_52w = None

        # Need basic price inputs
        if (
            asset.price is None
            or asset.high_52w is None
            or asset.low_52w is None
        ):
            continue

        # --- Calculate price moves ---
        asset.drop_52w = (asset.price - asset.high_52w) / asset.high_52w
        asset.gain_52w = (asset.price - asset.low_52w) / asset.low_52w

        if asset.low_years not in (None, 0):
            asset.gain_years = (asset.price - asset.low_years) / asset.low_years

        # --- Calculate realized CAGR for Calmar ---
        realized_cagr = None
        if (
            asset.gain_years is not None
            and years_rebound > 0
            and (1 + asset.gain_years) > 0
        ):
            realized_cagr = (1 + asset.gain_years) ** (1 / years_rebound) - 1

        # --- Calculate Calmar ratio ---
        if realized_cagr is not None and asset.mdd not in (None, 0):
            asset.calmar_ratio = realized_cagr / abs(asset.mdd)

        # Need signal inputs
        if asset.mdd is None or asset.rebound is None or asset.cagr is None:
            continue

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
