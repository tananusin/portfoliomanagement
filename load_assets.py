# load_assets.py
import pandas as pd
import streamlit as st
from asset_data import AssetData

def parse_yield(value):
    """Converts yield from string with '%' to float."""
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
    required_cols = {"name", "symbol", "currency", "shares", "price", "fx", "type", "52w_high", "52w_low", "3y_low", "pe", "yield"}
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
            asset_type=row["type"],
            peak_1y=row["52w_high"] if pd.notnull(row["52w_high"]) else 0.0,
            trough_1y=row["52w_low"] if pd.notnull(row["52w_low"]) else 0.0,
            trough_3y=row["3y_low"] if pd.notnull(row["3y_low"]) else 0.0,
            pe_ratio=row["pe"] if pd.notnull(row["pe"]) else 0.0,
            dividend_yield=parse_yield(row["yield"])                
        )
        for _, row in df.iterrows()
    ]

    return assets
