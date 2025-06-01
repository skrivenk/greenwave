# utils/formatter.py

def analyze_indicators(df) -> list:
    """
    Analyze indicators in the dataframe and return signal summaries.

    Parameters:
    - df: DataFrame containing columns like 'rsi', 'macd', 'signal', 'sma_14', 'price'

    Returns:
    - List of string summaries
    """
    messages = []

    # --- RSI Analysis ---
    if 'rsi' in df.columns and not df['rsi'].isna().all():
        latest_rsi = df['rsi'].dropna().iloc[-1]
        if latest_rsi > 70:
            messages.append(f"RSI is {latest_rsi:.1f} → Overbought (may suggest pullback)")
        elif latest_rsi < 30:
            messages.append(f"RSI is {latest_rsi:.1f} → Oversold (may suggest rebound)")
        else:
            messages.append(f"RSI is {latest_rsi:.1f} → Neutral")

    # --- MACD Analysis ---
    if 'macd' in df.columns and 'signal' in df.columns:
        macd = df['macd'].dropna().iloc[-1]
        signal = df['signal'].dropna().iloc[-1]
        if macd > signal:
            messages.append("MACD crossover → Bullish signal")
        elif macd < signal:
            messages.append("MACD crossover → Bearish signal")
        else:
            messages.append("MACD and Signal lines are equal → Neutral")

    # --- SMA Analysis ---
    if 'sma_14' in df.columns and 'price' in df.columns:
        latest_price = df['price'].dropna().iloc[-1]
        latest_sma = df['sma_14'].dropna().iloc[-1]
        if latest_price > latest_sma:
            messages.append(f"Price (${latest_price:.2f}) is above SMA-14 (${latest_sma:.2f}) → Uptrend")
        elif latest_price < latest_sma:
            messages.append(f"Price (${latest_price:.2f}) is below SMA-14 (${latest_sma:.2f}) → Downtrend")

    return messages
