# reserve_allocation.py

from typing import Iterable
from asset_data import AssetData
from currency_portfolio import Currency, build_currency_objects

def calculate_reserve_weights(cash_weight: float, user_pref,) -> tuple[float, float]:
    """
    Calculate bond and gold weights within reserve allocation.

    Logic:
        reserve_weight     = 1 - investment_weight
        gold_weight        = reserve_weight * gold_weight_reserve
        bond_weight_total  = reserve_weight - cash - gold

        If bond < 0 → reduce gold first
        If gold < 0 → insufficient reserve → raise error

    Returns:
        (bond_weight_total, gold_weight)
    """

    reserve_weight = 1 - user_pref.investment_weight
    gold_weight = reserve_weight * user_pref.gold_weight_reserve
    bond_weight_total = reserve_weight - cash_weight - gold_weight

    # Reduce gold first if reserve insufficient
    if bond_weight_total < 0:
        gold_weight += bond_weight_total
        bond_weight_total = 0.0

    return bond_weight_total, gold_weight

def build_currency_portfolio(assets: Iterable[AssetData], bond_weight_total: float,) -> tuple[list[Currency], dict[str, Currency]]:
    currency_names = [asset.currency for asset in assets if asset.currency]
    currencies, currency_map = build_currency_objects(currency_names)

    for asset in assets:
        if not asset.currency:
            continue

        currency_name = asset.currency.upper()
        target = asset.target or 0.0
        mdd = abs(asset.mdd) or 0.0

        ccy = currency_map[currency_name]
        ccy.currency_investment_weight += target
        ccy.currency_investment_mdd += target * mdd

    total_cash_weight = 0.0
    for ccy in currencies:
        ccy.currency_cash_weight = ccy.currency_investment_mdd
        total_cash_weight += ccy.currency_cash_weight

    for ccy in currencies:
        ccy.currency_cash_ratio = (
            ccy.currency_cash_weight / total_cash_weight
            if total_cash_weight > 0 else 0.0
        )
        ccy.currency_bond_weight = bond_weight_total * ccy.currency_cash_ratio

    return currencies, currency_map

def assign_reserve_asset_targets(
    assets: list[AssetData],
    currencies,
    gold_weight: float,
):
    """
    Assign target weights for Cash, Bond, and Gold assets.

    Cash and Bond targets are assigned per currency.
    Gold target is assigned globally.
    """

    # Build currency lookup
    currency_map = {c.name: c for c in currencies}

    # Count number of gold assets
    gold_assets = [a for a in assets if a.asset_class == "Gold"]
    n_gold = len(gold_assets)

    for asset in assets:

        # CASH
        if asset.asset_class == "Cash":
            ccy = currency_map.get(asset.currency.upper())
            if ccy:
                asset.target = ccy.currency_cash_weight

        # BOND
        elif asset.asset_class == "Bond":
            ccy = currency_map.get(asset.currency.upper())
            if ccy:
                asset.target = ccy.currency_bond_weight

        # GOLD
        elif asset.asset_class == "Gold":
            if n_gold > 0:
                asset.target = gold_weight / n_gold
