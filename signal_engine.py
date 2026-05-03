"""Score each ticker on trend + momentum + volume + breakout."""
import numpy as np
import pandas as pd


def rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0).rolling(period).mean()
    down = -delta.clip(upper=0).rolling(period).mean()
    rs = up / down.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


def atr(df, period=14):
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift()).abs()
    low_close = (df["Low"] - df["Close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def score_ticker(ticker, df, min_score=50):
    if df is None or len(df) < 60:
        return None

    close = df["Close"]
    volume = df["Volume"]

    ema20 = ema(close, 20)
    ema50 = ema(close, 50)
    rsi_val = rsi(close, 14)
    atr_val = atr(df, 14)

    if pd.isna(ema50.iloc[-1]) or pd.isna(rsi_val.iloc[-1]) or pd.isna(atr_val.iloc[-1]):
        return None

    price = float(close.iloc[-1])
    ema20_now = float(ema20.iloc[-1])
    ema50_now = float(ema50.iloc[-1])
    rsi_now = float(rsi_val.iloc[-1])
    atr_now = float(atr_val.iloc[-1])

    score = 0
    reasons = []

    if price > ema50_now:
        score += 25
        reasons.append("Trend yukarı (fiyat > EMA50)")

    if ema20_now > ema50_now:
        score += 20
        reasons.append("Kısa vadeli momentum pozitif (EMA20 > EMA50)")

    if 50 <= rsi_now <= 70:
        score += 25
        reasons.append(f"RSI güçlü ({rsi_now:.1f})")
    elif 40 <= rsi_now < 50:
        score += 10
        reasons.append(f"RSI nötr ({rsi_now:.1f})")

    avg_vol = volume.rolling(20).mean().iloc[-1]
    if not pd.isna(avg_vol) and float(volume.iloc[-1]) > float(avg_vol):
        score += 15
        reasons.append("Hacim ortalamanın üzerinde")

    high_20 = close.rolling(20).max().iloc[-1]
    if not pd.isna(high_20) and price >= float(high_20) * 0.98:
        score += 15
        reasons.append("20 günlük zirveye yakın")

    if score < min_score:
        return None

    return {
        "ticker": ticker,
        "score": score,
        "price": price,
        "rsi": rsi_now,
        "atr": atr_now,
        "ema20": ema20_now,
        "ema50": ema50_now,
        "reasons": reasons,
    }


def generate_signals(price_data, min_score=50):
    signals = [
        s for ticker, df in price_data.items()
        if (s := score_ticker(ticker, df, min_score)) is not None
    ]
    signals.sort(key=lambda x: x["score"], reverse=True)
    return signals
