# class_portfolio.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class RiskClass:
    name: str
    class_mdd: Optional[float] = None
    class_mdd_inverse: Optional[float] = None
    class_target_weight: Optional[float] = None
    class_mdd_contribution: Optional[float] = None

# ERC investment classes only
ERC_CLASSES = ["Core", "Growth", "Speculative"]

# Risk classes used in hierarchical ERC
RISK_CLASSES = [
    RiskClass("Core"),
    RiskClass("Growth"),
    RiskClass("Speculative"),
]
