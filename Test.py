from dataclasses import dataclass, field
from typing import List

@dataclass
class StockData:
    ticker: str
    price_history: List[float] = field(default_factory=list)
    net_profit_history: List[float] = field(default_factory=list)
    dividend_yield: float = 0.0
