# portfolio_value.py
from typing import List
from asset_data import AssetData
from fetch_yfinance import get_price, get_fx_to_thb, get_52_week_high, get_52_week_low, get_trailing_pe, get_trailing_dividend_yield


def calculate_asset_values(asset: AssetData) -> None:
    """
    Compute value_local and value_thb for an asset if price and fx_rate are available.
    """
    if asset.price is not None and asset.fx_rate is not None:
        asset.value_local = asset.shares * asset.price
        asset.value_thb = asset.value_local * asset.fx_rate


def enrich_asset(asset: AssetData) -> AssetData:
    """
    Fetch price and fx_rate for an asset and compute its values.
    """
    # FX rate
    if asset.currency == 'THB':
        asset.fx_rate = 1
    else:
        asset.fx_rate = get_fx_to_thb(asset.currency)

    # Price handling
    if asset.symbol == 'CASH':
        asset.price = 1
    elif asset.symbol == 'BOND':
        pass  # Use user-assigned value
    elif asset.symbol == 'FUNDTH':
        pass  # Use user-assigned value
    else:
        asset.price = get_price(asset.symbol)
        asset.high_52w = get_52_week_high(asset.symbol)
        asset.low_52w = get_52_week_low(asset.symbol)
        asset.pe_ratio = get_trailing_pe(asset.symbol)
        asset.dividend_yield = get_trailing_dividend_yield(asset.symbol)

    # Calculate value
    calculate_asset_values(asset)
    return asset


def enrich_assets(assets: List[AssetData]) -> List[AssetData]:
    return [enrich_asset(asset) for asset in assets]


def summarize_assets(assets: List[AssetData]) -> List[AssetData]:
    """
    Combine bonds and cash into summary positions. Recalculate values if needed.
    """
    # Ensure all value fields are populated
    for asset in assets:
        calculate_asset_values(asset)

    # Categorize
    bond_assets = [a for a in assets if a.asset_type == "Bond"]
    cash_assets = [a for a in assets if a.asset_type == "Cash"]
    other_assets = [a for a in assets if a.asset_type not in {"Cash", "Bond"}]

    def _summarize_group(assets_to_sum, name, asset_type):
        total_value_thb = sum(a.value_thb or 0 for a in assets_to_sum)
        if total_value_thb == 0:
            return None
        return AssetData(
            name=name,
            symbol=name.upper().replace(" ", "_"),
            currency="THB",
            shares=1,
            price=1,
            asset_type=asset_type,
            fx_rate=1,
            value_local=total_value_thb,
            value_thb=total_value_thb,
        )

    summarized = []
    total_bond = _summarize_group(bond_assets, "Total Bond", "Bond")
    total_cash = _summarize_group(cash_assets, "Total Cash", "Cash")

    if total_bond:
        summarized.append(total_bond)
    if total_cash:
        summarized.append(total_cash)

    return other_assets + summarized


def calculate_portfolio_total(assets: List[AssetData]) -> float:
    return sum(asset.value_thb or 0 for asset in assets)


def assign_weights(assets: List[AssetData], total_value: float):
    for asset in assets:
        if asset.value_thb is not None and total_value > 0:
            asset.weight = asset.value_thb / total_value
