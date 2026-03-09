# yield_signal.py
from typing import List
from asset_data import AssetData


def assign_yield_signals(assets: List[AssetData]) -> List[AssetData]:
    """
    Evaluate dividend yield sufficiency relative to expected recovery offset.
    """

    for asset in assets:

        # Only apply to investment assets
        if asset.asset_class not in {"Core", "Growth", "Speculative"}:
            asset.dividend_yield_signal = None
            continue

        # Need assumption + yield
        if asset.dividend_yield is None or asset.dividend_yield_offset is None:
            asset.dividend_yield_signal = None
            continue

        # Compare yield vs offset
        if asset.dividend_yield >= asset.dividend_yield_offset:
            asset.dividend_yield_signal = "sufficient"
        else:
            asset.dividend_yield_signal = "-"

    return assets
