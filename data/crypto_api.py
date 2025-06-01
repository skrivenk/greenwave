# data/crypto_api.py

import requests
import pandas as pd
from datetime import datetime

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Map app dropdown timeframe to CoinGecko params
TIMEFRAMES = {
    "1D": 1,
    "1W": 7,
    "1M": 30,
    "6M": 180,
    "1Y": 365
}

def fetch_market_chart(coin_id: str, vs_currency: str = "usd", days: str = "30") -> pd.DataFrame:
    """
    Fetch historical market data for a given coin.
    """
    url = f"{COINGECKO_BASE_URL}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days,
        "interval": "hourly" if int(days) <= 7 else "daily"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    data = response.json()
    prices = data.get("prices", [])

    # Convert to DataFrame
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit='ms')
    df.set_index("date", inplace=True)
    df.drop(columns=["timestamp"], inplace=True)

    return df


def get_supported_coins() -> list:
    """
    Get list of supported coins and their IDs.
    """
    url = f"{COINGECKO_BASE_URL}/coins/list"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch coin list.")

    return response.json()


def map_symbol_to_id(symbol: str) -> str:
    """
    Convert coin symbol (e.g., 'BTC') to CoinGecko ID (e.g., 'bitcoin').
    """
    coins = get_supported_coins()
    for coin in coins:
        if coin["symbol"].lower() == symbol.lower():
            return coin["id"]
    raise ValueError(f"Symbol {symbol} not found in CoinGecko list.")
