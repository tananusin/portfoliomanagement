# yield_signal.py
from typing import List
from asset_data import AssetData
from user_preferences import UserPreference
import streamlit as st

def print_ABC():
    st.write("ABC")

def assign_yield_signals(
    assets: List[AssetData],
    yield_thresholds: dict
) -> List[AssetData]:
    for asset in assets:
        if asset.asset_type is None:
            continue

        threshold = yield_thresholds.get(asset.asset_type)
        if threshold is None:
            asset.dividend_yield_signal = None
            continue

        asset.dividend_yield_recovery = threshold

        if asset.dividend_yield is not None and asset.dividend_yield >= threshold:
            asset.dividend_yield_signal = "sufficient"
        else:
            asset.dividend_yield_signal = "insufficient"

    return assets
