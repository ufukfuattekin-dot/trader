"""Fetch OHLCV data for a list of tickers using yfinance."""
import pandas as pd
import yfinance as yf
import time

# MAG
DEFAULT_TICKERS = [
    "AAPL", "MSFT", "NVDA", "TSLA"
]


# 🔥 YENİ: güvenli veri çekme (retry + hata toleransı)
def get_data(ticker, period="6mo", interval="1d"):
    for i in range(3):  # 3 kez dene
        try:
            print(f"İşleniyor: {ticker}")

            df = yf.download(
                ticker,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=True,
            )

            if df is not None and not df.empty and len(df) > 50:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                return df.dropna()

        except Exception as e:
            print(f"HATA: {ticker} → {e}")
            time.sleep(2)

    print(f"FAIL: {ticker}")
    return None


# 🔥 YENİ: tek tek çek (toplu değil)
def fetch_data(tickers, period="6mo", interval="1d"):
    if isinstance(tickers, str):
        tickers = [tickers]

    results = {}

    for ticker in tickers:
        df = get_data(ticker, period, interval)

        if df is not None:
            results[ticker] = df

    return results


def scan(tickers=None):
    return fetch_data(tickers or DEFAULT_TICKERS)
