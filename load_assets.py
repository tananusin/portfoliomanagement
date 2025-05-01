# load_assets.py
import pandas as pd
import streamlit as st
from asset_data import AssetData

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
    required_cols = {"name", "symbol", "currency", "shares", "price", "fx", "type"}
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
        )
        for _, row in df.iterrows()
    ]

    return assets
