# portfolio_value.py
from fetch import get_price, get_fx_to_thb
from asset_data import AssetData
from typing import List

def enrich_asset(asset: AssetData) -> AssetData:
    # Handle THB currency first, set fx_rate to 1
    if asset.currency == 'THB':
        asset.fx_rate = 1
    else:
        # For other currencies, fetch fx_rate normally
        asset.fx_rate = get_fx_to_thb(asset.currency)

    # Handle BOND and CASH symbols
    if asset.symbol == 'CASH':
        asset.price = 1
    elif asset.symbol == 'BOND':
        pass  # keep asset.price as user-assigned (or asset.par assigned earlier)
    else:
        # For other assets, fetch price normally
        asset.price = get_price(asset.symbol)
    
    # Calculate value if price and fx_rate are valid
    if asset.price is not None and asset.fx_rate is not None:
        asset.value_local = asset.shares * asset.price
        asset.value_thb = asset.value_local * asset.fx_rate
    
    return asset

def enrich_assets(assets: List[AssetData]) -> List[AssetData]:
    enriched = [enrich_asset(asset) for asset in assets]

    # Separate asset types for summarize Bond and Cash asset type
    bond_assets = [a for a in enriched if a.asset_type == "Bond"]
    cash_assets = [a for a in enriched if a.asset_type == "Cash"]
    other_assets = [a for a in enriched if a.asset_type not in {"Cash", "Bond"}]

    def summarize_assets(assets_to_sum, name, asset_type):
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
    total_bond = summarize_assets(bond_assets, "Total Bond", "Bond")
    total_cash = summarize_assets(cash_assets, "Total Cash", "Cash")
    if total_bond:
        summarized.append(total_bond)
    if total_cash:
        summarized.append(total_cash)

    # Return combined list
    return other_assets + summarized

def calculate_portfolio_total(assets: List[AssetData]) -> float:
    return sum(asset.value_thb or 0 for asset in assets)

def assign_weights(assets: List[AssetData], total_value: float):
    for asset in assets:
        if asset.value_thb is not None:
            asset.weight = asset.value_thb / total_value
