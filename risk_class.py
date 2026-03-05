from dataclasses import dataclass


@dataclass
class RiskClass:
    name: str
    class_mdd: float
    class_target_weight: float | None = None
    class_mdd_inverse: float | None = None
