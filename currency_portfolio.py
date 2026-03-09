#currency_portfolio.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class Currency:
    name: str

    # Investment-side currency exposure
    currency_investment_weight: Optional[float] = None
    currency_investment_mdd: Optional[float] = None

    # Reserve-side allocation
    currency_cash_weight: Optional[float] = None
    currency_cash_ratio: Optional[float] = None
    currency_bond_weight: Optional[float] = None


def build_currency_objects(currency_names: list[str]):
    currencies = [Currency(name=n) for n in currency_names]
    currency_map = {c.name: c for c in currencies}
    return currencies, currency_map
