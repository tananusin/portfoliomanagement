from dataclasses import dataclass


@dataclass
class PortfolioConfig:
    investment_weight: float = 0.5
    gold_weight_reserve: float = 0.2

    years_rebound: int = 3
    years_dividend: int = 5

    threshold_drift: float = 0.05
    threshold_drift_relative: float = 0.5
