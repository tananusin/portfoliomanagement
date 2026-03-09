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


def build_currency_map(currency_names: list[str]) -> dict[str, Currency]:
    return {name: Currency(name=name) for name in currency_names}
