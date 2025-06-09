import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

def get_ebay_access_token(client_id, client_secret):
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {requests.auth._basic_auth_str(client_id, client_secret)}"
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
    url = (
        f"https://api.ebay.com/buy/marketplace_insights/v1/item_sales/search?"
        f"q={player_name}&filter=transactionDate:[{date_from}..]"
    )

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
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
