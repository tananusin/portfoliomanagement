from dataclasses import dataclass
from typing import Optional

@dataclass
class AssetData:
    name: str
    symbol: str
    currency: str
    shares: float
    target: Optional[float] = None
    asset_type: Optional[str] = None

    price: Optional[float] = None
    fx_rate: Optional[float] = None
    value_local: Optional[float] = None
    value_thb: Optional[float] = None
    portfolio_total: Optional[float] = None
    weight: Optional[float] = None

    def compute_value(self):
        if self.price is not None and self.fx_rate is not None:
            self.value_local = self.shares * self.price
            self.value_thb = self.value_local * self.fx_rate

    def compute_weight(self):
        if self.value_thb is not None and self.portfolio_total:
            self.weight = self.value_thb / self.portfolio_total