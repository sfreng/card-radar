import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from urllib.parse import quote
import base64

def get_ebay_access_token(client_id, client_secret):
    url = "https://api.ebay.com/identity/v1/oauth2/token"

    # Genera manualmente la stringa base64
    credentials = f"{client_id}:{client_secret}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        st.error(f"❌ Errore API eBay: {response.status_code} – {response.text}")
        st.stop()

    return response.json()["access_token"]

def fetch_ebay_sales(player_name, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    days_back = 90
    date_from = (datetime.utcnow() - timedelta(days=days_back)).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Codifica sicura del nome
    search_query = quote(player_name.lower())

    url = (
        f"https://api.ebay.com/buy/marketplace_insights/v1/item_sales/search?"
        f"q={search_query}&filter=transactionDate:[{date_from}..]"
    )

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.warning(f"⚠️ Nessun risultato per {player_name} (Errore {response.status_code})")
        return []
    
    data = response.json()
    results = []
    for item in data.get("itemSales", []):
        results.append({
            "Giocatore": player_name,
            "Titolo": item.get("title", ""),
            "Prezzo": float(item["price"]["value"]),
            "Valuta": item["price"]["currency"],
            "Data Vendita": item["transactionDate"],
            "Link": item["itemAffiliateWebUrl"]
        })
    return results
