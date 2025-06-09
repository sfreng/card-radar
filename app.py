import streamlit as st
import pandas as pd
from sales_fetcher import get_ebay_access_token, fetch_ebay_sales
import os

st.set_page_config(page_title="Card Radar", layout="wide")
st.title("📊 Card Radar – Vendite eBay concluse")

# Leggi chiavi dal secrets.toml
CLIENT_ID = st.secrets["EBAY_CLIENT_ID"]
CLIENT_SECRET = st.secrets["EBAY_CLIENT_SECRET"]
st.write("Client ID:", CLIENT_ID[:10])  # Debug visivo temporaneo

# Carica wishlist
with open("wishlist_updated.txt", "r") as f:
    players = [line.strip() for line in f if line.strip()]

access_token = get_ebay_access_token(CLIENT_ID, CLIENT_SECRET)

all_results = []
with st.spinner("⏳ Recupero vendite per ogni giocatore..."):
    for player in players:
        results = fetch_ebay_sales(player, access_token)
        all_results.extend(results)

df = pd.DataFrame(all_results)
if not df.empty:
    df["Prezzo"] = df["Prezzo"].astype(float)
    st.success(f"Trovate {len(df)} vendite.")
    st.dataframe(df)
    df.to_csv("data/sales_data.csv", index=False)
else:
    st.warning("Nessuna vendita trovata.")

