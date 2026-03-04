# load_assets.py
import pandas as pd
import streamlit as st
from asset_data import AssetData

def parse_percent(value):
    """Converts percent from string with '%' to float."""
    try:
        if isinstance(value, str) and "%" in value:
            return float(value.replace("%", "").strip()) / 100
        return float(value) if pd.notnull(value) else 0.0
    except (ValueError, TypeError):
        return 0.0

def load_assets_from_google_sheet(sheet_url: str) -> list[AssetData]:
    # Adjust URL for CSV export
    sheet_url = sheet_url.replace('/edit#gid=', '/gviz/tq?tqx=out:csv&gid=')

    # Load and clean data
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip().str.lower()
    except Exception as e:
        st.error(f"❌ Failed to load Google Sheet: {e}")
        st.stop()

    # Validate columns
    required_cols = {"name", "symbol", "currency", "shares", "price", "fx", "class", "mdd", "52w high", "52w low", "years low", "pe", "pe p25", "pe p75", "yield"}
    if not required_cols.issubset(df.columns):
        st.error(f"Missing columns in Google Sheet. Required: {required_cols}")
        st.write("Loaded columns:", df.columns.tolist())
        st.stop()

    # Create AssetData objects
    assets = [
        AssetData(
            name=row["name"],
            symbol=row["symbol"],
            currency=row["currency"],
            shares=row["shares"],
            price=row["price"] if pd.notnull(row["price"]) else 0.0,
            fx_rate=row["fx"] if pd.notnull(row["fx"]) else 0.0,
            asset_class=row["class"],
            mdd=parse_percent(row["mdd"])          
            high_52w=row["52w high"] if pd.notnull(row["52w high"]) else 0.0,
            low_52w=row["52w low"] if pd.notnull(row["52w low"]) else 0.0,
            low_years=row["years low"] if pd.notnull(row["years low"]) else 0.0,
            pe_ratio=row["pe"] if pd.notnull(row["pe"]) else 0.0,
            pe_p25=row["pe p25"] if pd.notnull(row["pe p25"]) else 0.0,
            pe_p75=row["pe p75"] if pd.notnull(row["pe p75"]) else 0.0,
            dividend_yield=parse_percent(row["yield"])                
        )
        for _, row in df.iterrows()
    ]

    return assets
