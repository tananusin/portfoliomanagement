# yield_signal.py
from typing import List
from asset_data import AssetData
from user_preferences import UserPreference

def assign_yield_signals(assets: List[AssetData], prefs: UserPreference) -> List[AssetData]:

    for asset in assets:
        if asset.asset_type is None:
            continue

        # Assign offset based on asset type
        if asset.asset_type == "Speculative":
            asset.dividend_yield_offset = prefs.yield_speculative / 100
        elif asset.asset_type == "Growth":
            asset.dividend_yield_offset = prefs.yield_growth / 100
        elif asset.asset_type == "Core":
            asset.dividend_yield_offset = prefs.yield_core / 100
        else:
            asset.dividend_yield_signal = None
            continue

        # Adjust offset if drop_1y is more severe
        if asset.drop_1y is not None and asset.dividend_yield_offset < (asset.drop_1y / -5):
            asset.dividend_yield_offset = asset.drop_1y / -5

        # Compare yield vs. offset
        if asset.dividend_yield is not None and asset.dividend_yield >= asset.dividend_yield_offset:
            asset.dividend_yield_signal = "sufficient"
        else:
            asset.dividend_yield_signal = "-"

    return assets
