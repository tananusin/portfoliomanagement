# load_assets.py
import pandas as pd
import streamlit as st
from asset_data import AssetData


def parse_percent(value) -> float:
    """Converts percent from string with '%' to float (e.g., '5%' -> 0.05)."""
    try:
        if isinstance(value, str):
            v = value.strip()
            if v.endswith("%"):
                return float(v[:-1].strip()) / 100.0
            return float(v)
        return float(value) if pd.notna(value) else 0.0
    except (ValueError, TypeError):
        return 0.0


def parse_float(value) -> float:
    """Safely convert to float; return 0.0 for NaN/None/bad values."""
    try:
        return float(value) if pd.notna(value) else 0.0
    except (ValueError, TypeError):
        return 0.0


def load_assets_from_google_sheet(sheet_url: str) -> list[AssetData]:
    # Adjust URL for CSV export
    sheet_url = sheet_url.replace("/edit#gid=", "/gviz/tq?tqx=out:csv&gid=")

    # Load and clean data
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip().str.lower()
    except Exception as e:
        st.error(f"❌ Failed to load Google Sheet: {e}")
        st.stop()

    # Validate columns
    required_cols = {
        "name", "symbol", "currency", "shares", "price", "fx", "class", "assumed mdd",
        "52w high", "52w low", "years low", "pe", "pe p25", "pe p75", "yield"
    }

    missing = required_cols - set(df.columns)
    if missing:
        st.error(f"Missing columns in Google Sheet: {sorted(missing)}")
        st.write("Loaded columns:", df.columns.tolist())
        st.stop()

    # Create AssetData objects
    assets = [
        AssetData(
            name=row["name"],
            symbol=row["symbol"],
            currency=row["currency"],
            shares=parse_float(row["shares"]),
            price=parse_float(row["price"]),
            fx_rate=parse_float(row["fx"]),
            asset_class=row["class"],
            mdd=parse_percent(row["assumed mdd"]),
            high_52w=parse_float(row["52w high"]),
            low_52w=parse_float(row["52w low"]),
            low_years=parse_float(row["years low"]),
            pe_ratio=parse_float(row["pe"]),
            pe_p25=parse_float(row["pe p25"]),
            pe_p75=parse_float(row["pe p75"]),
            dividend_yield=parse_percent(row["yield"]),
        )
        for _, row in df.iterrows()
    ]

    return assets
