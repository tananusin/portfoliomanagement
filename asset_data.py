# asset_data.py
from dataclasses import dataclass
from typing import Optional  # If User Leave Input Empty

@dataclass
class AssetData:
    # Google Sheet Variables
    name: str
    symbol: str
    currency: str
    shares: float
    price: Optional[float] = None
    fx_rate: Optional[float] = None
    asset_type: Optional[str] = None

    # Portfolio Value Variables
    value_local: Optional[float] = None
    value_thb: Optional[float] = None
    weight: Optional[float] = None

    # Proportion
    target: Optional[float] = None

    # Position Size
    drift: Optional[float] = None
    drift_pct: Optional[float] = None
    position_size: Optional[str] = None

    # Price Change
    high_52w: Optional[float] = None
    low_52w: Optional[float] = None
    low_3y: Optional[float] = None
    drop_1y: Optional[float] = None
    gain_1y: Optional[float] = None
    gain_3y: Optional[float] = None
    price_change: Optional[str] = None

    # Fundamental Ratios
    pe_ratio: Optional[float] = None            # Trailing P/E ratio
    pe_p25: Optional[float] = None              # 25th percentile P/E
    pe_p75: Optional[float] = None              # 75th percentile P/E
    pe_signal: Optional[str] = None
    
    dividend_yield: Optional[float] = None      # Trailing dividend yield
