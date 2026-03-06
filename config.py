#config.py
from dataclasses import dataclass

@dataclass
class RiskClass:
    name: str
    class_mdd: float  # decimal, e.g. -0.25
    class_mdd_inverse: float

# Drift thresholds (decimals)
THRESHOLD_DRIFT = 0.05
THRESHOLD_DRIFT_RELATIVE = 0.50

# Default class assumptions
RISK_CLASSES = [
    RiskClass("Core", -0.25, 4.0),
    RiskClass("Growth", -0.50, 2.0),
    RiskClass("Speculative", -0.70, 1.43),
]
