# erc.py
from typing import Any, Iterable


def apply_erc_by_mdd(
    items: Iterable[Any],
    mdd_attr: str,
    inverse_attr: str,
    target_attr: str,
) -> float:
    """
    Generic Equal Risk Contribution (ERC) using inverse MDD.

    Formula:
        Inverse MDD       = 1 / assumed MDD
        Total Inverse MDD = Σ(Inverse MDD)
        Target Weight     = Inverse MDD / Total Inverse MDD
        Portfolio MDD     = Σ(Target Weight × assumed MDD)

    Notes:
        - MDD can be negative or positive; abs(MDD) is used.
        - Mutates each item by writing inverse_attr and target_attr.

    Returns:
        float: weighted portfolio MDD
    """
    items = list(items)

    if not items:
        raise ValueError("No items provided for ERC calculation.")

    total_inverse_mdd = 0.0

    for item in items:
        raw_mdd = getattr(item, mdd_attr, None)

        if raw_mdd is None:
            raise ValueError(
                f"{getattr(item, 'name', getattr(item, 'ticker', item))} "
                f"has no attribute '{mdd_attr}'"
            )

        mdd = abs(raw_mdd)
        if mdd <= 0:
            raise ValueError(
                f"{getattr(item, 'name', getattr(item, 'ticker', item))} "
                f"has invalid {mdd_attr}={raw_mdd}. MDD must be non-zero."
            )

        inverse_mdd = 1 / mdd
        setattr(item, inverse_attr, inverse_mdd)
        total_inverse_mdd += inverse_mdd

    if total_inverse_mdd <= 0:
        raise ValueError("Total inverse MDD must be greater than 0.")

    for item in items:
        inverse_mdd = getattr(item, inverse_attr)
        target_weight = inverse_mdd / total_inverse_mdd
        setattr(item, target_attr, target_weight)

    portfolio_mdd = 0.0
    for item in items:
        mdd = abs(getattr(item, mdd_attr))
        target_weight = getattr(item, target_attr)
        portfolio_mdd += target_weight * mdd

    return portfolio_mdd


def apply_asset_class_erc(assets, risk_classes, class_name: str) -> float:
    """
    Apply ERC to assets within one class, then write the resulting
    weighted class MDD back to the matching RiskClass.class_mdd.

    Writes:
        asset.mdd_inverse
        asset.target_in_class
        risk_class.class_mdd

    Returns:
        float: weighted MDD of the class
    """
    class_assets = [a for a in assets if a.asset_class == class_name]

    if not class_assets:
        raise ValueError(f"No assets found in asset_class='{class_name}'")

    class_mdd = apply_erc_by_mdd(
        items=class_assets,
        mdd_attr="mdd",
        inverse_attr="mdd_inverse",
        target_attr="target_in_class",
    )

    matched = False
    for rc in risk_classes:
        if rc.name == class_name:
            rc.class_mdd = class_mdd
            matched = True
            break

    if not matched:
        raise ValueError(f"No RiskClass found with name='{class_name}'")

    return class_mdd


def apply_all_asset_class_erc(assets, risk_classes) -> None:
    """
    Run ERC for every class defined in risk_classes.
    """
    for rc in risk_classes:
        apply_asset_class_erc(assets, risk_classes, rc.name)


def apply_risk_class_erc(risk_classes) -> float:
    """
    Apply ERC across portfolio classes using dynamically computed class_mdd.

    Writes:
        risk_class.class_mdd_inverse
        risk_class.class_target_weight

    Returns:
        float: weighted MDD across classes
    """
    return apply_erc_by_mdd(
        items=risk_classes,
        mdd_attr="class_mdd",
        inverse_attr="class_mdd_inverse",
        target_attr="class_target_weight",
    )


def apply_final_asset_targets(assets, risk_classes) -> None:
    """
    Final portfolio target per asset:
        asset.target = class_target_weight × target_in_class
    """
    class_map = {rc.name: rc.class_target_weight for rc in risk_classes}

    for asset in assets:
        if asset.asset_class not in class_map:
            raise ValueError(
                f"Unknown asset_class='{asset.asset_class}' "
                f"for asset '{asset.ticker}'"
            )

        class_weight = class_map[asset.asset_class]
        if class_weight is None:
            raise ValueError(
                f"Risk class '{asset.asset_class}' has no class_target_weight. "
                "Run apply_risk_class_erc() first."
            )

        if asset.target_in_class is None:
            raise ValueError(
                f"Asset '{asset.ticker}' has no target_in_class. "
                f"Run asset ERC first for class '{asset.asset_class}'."
            )

        asset.target = class_weight * asset.target_in_class
