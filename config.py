#config.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class RiskClass:
    name: str
    class_mdd: Optional[float] = None
    class_mdd_inverse: Optional[float] = None
    class_target_weight: Optional[float] = None

# Drift thresholds (decimals)
THRESHOLD_DRIFT = 0.05
THRESHOLD_DRIFT_RELATIVE = 0.50

# Default class assumptions
RISK_CLASSES = [
    RiskClass("Core"),
    RiskClass("Growth"),
    RiskClass("Speculative"),
]
