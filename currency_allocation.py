# currency_allocation.py

from typing import Iterable
from asset_data import AssetData
from currency_portfolio import Currency, build_currency_objects


def build_currency_portfolio(assets: Iterable[AssetData], bond_weight_total: float,) -> tuple[list[Currency], dict[str, Currency]]:
    currency_names = [asset.currency for asset in assets if asset.currency]
    currencies, currency_map = build_currency_objects(currency_names)

    for asset in assets:
        if not asset.currency:
            continue

        currency_name = asset.currency.upper()
        target = asset.target or 0.0
        mdd = asset.mdd or 0.0

        ccy = currency_map[currency_name]
        ccy.currency_investment_weight += target
        ccy.currency_investment_mdd += target * mdd

    total_cash_weight = 0.0
    for ccy in currencies:
        ccy.currency_cash_weight = abs(ccy.currency_investment_mdd)
        total_cash_weight += ccy.currency_cash_weight

    for ccy in currencies:
        ccy.currency_cash_ratio = (
            ccy.currency_cash_weight / total_cash_weight
            if total_cash_weight > 0 else 0.0
        )
        ccy.currency_bond_weight = bond_weight_total * ccy.currency_cash_ratio

    return currencies, currency_map
