# charts/plotter.py

import pandas as pd
from matplotlib.figure import Figure
import pandas_ta as ta


def plot_price_with_indicators(df: pd.DataFrame, indicators: dict) -> Figure:
    """
    Create a matplotlib figure with price and selected indicators.

    Parameters:
    - df: DataFrame with price column and datetime index
    - indicators: dict like {"rsi": True, "macd": True, "sma": True}

    Returns:
    - Matplotlib Figure
    """
    fig = Figure(figsize=(10, 6))
    ax_price = fig.add_subplot(2, 1, 1)
    ax_price.set_title("Crypto Price Chart")
    ax_price.plot(df.index, df["price"], label="Price", color="#228B22")  # Forest green

    # SMA/EMA overlays
    if indicators.get("sma", False):
        df["sma_14"] = ta.sma(df["price"], length=14)
        df["ema_14"] = ta.ema(df["price"], length=14)
        ax_price.plot(df.index, df["sma_14"], label="SMA 14", linestyle="--", color="#93C572")
        ax_price.plot(df.index, df["ema_14"], label="EMA 14", linestyle=":", color="#ADEBB3")

    ax_price.legend(loc="upper left")
    ax_price.grid(True)

    # RSI subplot
    if indicators.get("rsi", False):
        ax_rsi = fig.add_subplot(2, 2, 3, sharex=ax_price)
        df["rsi"] = ta.rsi(df["price"], length=14)
        ax_rsi.plot(df.index, df["rsi"], label="RSI", color="#36454F")
        ax_rsi.axhline(70, linestyle="--", color="red", alpha=0.3)
        ax_rsi.axhline(30, linestyle="--", color="green", alpha=0.3)
        ax_rsi.set_ylabel("RSI")
        ax_rsi.legend()
        ax_rsi.grid(True)

    # MACD subplot
    if indicators.get("macd", False):
        ax_macd = fig.add_subplot(2, 2, 4, sharex=ax_price)
        macd = ta.macd(df["price"])
        df["macd"] = macd["MACD_12_26_9"]
        df["signal"] = macd["MACDs_12_26_9"]
        ax_macd.plot(df.index, df["macd"], label="MACD", color="#228B22")
        ax_macd.plot(df.index, df["signal"], label="Signal", color="#36454F")
        ax_macd.legend()
        ax_macd.grid(True)

    fig.tight_layout()
    return fig
