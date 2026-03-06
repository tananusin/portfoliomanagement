# assumption.py

from typing import Optional
from asset_data import AssetData
from user_preferences import UserPreference


def calculate_assumptions(asset: AssetData, user_pref: UserPreference) -> None:
    # Calculate future return assumptions for an asset. Results are stored directly inside AssetData.

    if asset.price is None:
        return

    # Rebound
    if asset.fair_price is not None:
        asset.rebound = asset.fair_price / asset.price - 1

    # CAGR
    if asset.rebound is not None:

        years = user_pref.years_rebound

        asset.cagr = (1 + asset.rebound) ** (1 / years) - 1

    # Dividend Yield Offset
    if asset.dividend_yield is not None and user_pref.risk_free_rate is not None:

        asset.dividend_yield_offset = (
            asset.dividend_yield - user_pref.risk_free_rate
        )
