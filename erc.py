# erc.py
from typing import Any, Iterable


def apply_erc_by_mdd(
    items: Iterable[Any],
    mdd_attr: str,
    inverse_attr: str,
    target_attr: str,
) -> float:
    """
    Generic Equal Risk Contribution using inverse MDD.

    Formula:
        Inverse MDD      = 1 / assumed MDD
        Total Inverse    = Σ(Inverse MDD)
        Target Weight    = Inverse MDD / Total Inverse MDD
        Portfolio MDD    = Σ(Target Weight × assumed MDD)

    This function mutates each item by writing:
        - inverse_attr
        - target_attr

    Returns:
        portfolio_mdd (float)
    """
    items = list(items)

    # 1) Calculate inverse MDD
    total_inverse_mdd = 0.0
    for item in items:
        raw_mdd = getattr(item, mdd_attr, None)

        if raw_mdd is None:
            raise ValueError(f"{getattr(item, 'name', item)} has no {mdd_attr}")

        mdd = abs(raw_mdd)
        if mdd <= 0:
            raise ValueError(
                f"{getattr(item, 'name', item)} has invalid {mdd_attr}={raw_mdd}. "
                "MDD must be non-zero."
            )

        inverse_mdd = 1 / mdd
        setattr(item, inverse_attr, inverse_mdd)
        total_inverse_mdd += inverse_mdd

    if total_inverse_mdd <= 0:
        raise ValueError("Total inverse MDD must be greater than 0.")

    # 2) Calculate target weights
    for item in items:
        inverse_mdd = getattr(item, inverse_attr)
        target_weight = inverse_mdd / total_inverse_mdd
        setattr(item, target_attr, target_weight)

    # 3) Calculate portfolio MDD
    portfolio_mdd = 0.0
    for item in items:
        mdd = abs(getattr(item, mdd_attr))
        target_weight = getattr(item, target_attr)
        portfolio_mdd += target_weight * mdd

    return portfolio_mdd


def apply_asset_class_erc(assets, class_name: str) -> float:
    class_assets = [a for a in assets if a.asset_class == class_name]
    return apply_erc_by_mdd(
        items=class_assets,
        mdd_attr="mdd",
        inverse_attr="mdd_inverse",
        target_attr="target_in_class",
    )

def apply_risk_class_erc(risk_classes) -> float:
    return apply_erc_by_mdd(
        items=risk_classes,
        mdd_attr="class_mdd",
        inverse_attr="class_mdd_inverse",
        target_attr="target_weight",
    )
