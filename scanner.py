"""Fetch OHLCV data for a list of tickers using yfinance."""
import pandas as pd
import yfinance as yf

# BIST 30 — large-cap Turkish stocks (yfinance suffix .IS)
DEFAULT_TICKERS = [
    "AKBNK.IS", "ARCLK.IS", "ASELS.IS", "BIMAS.IS", "EREGL.IS",
    "FROTO.IS", "GARAN.IS", "ISCTR.IS", "KCHOL.IS", "KOZAL.IS",
    "PETKM.IS", "PGSUS.IS", "SAHOL.IS", "SASA.IS", "SISE.IS",
    "TAVHL.IS", "TCELL.IS", "THYAO.IS", "TOASO.IS", "TUPRS.IS",
    "VAKBN.IS", "YKBNK.IS",
]


def fetch_data(tickers, period="6mo", interval="1d"):
    if isinstance(tickers, str):
        tickers = [tickers]

    if len(tickers) == 1:
        df = yf.download(
            tickers[0], period=period, interval=interval,
            progress=False, auto_adjust=True,
        )
        if df is None or df.empty:
            return {}
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return {tickers[0]: df.dropna()} if len(df) > 50 else {}

    raw = yf.download(
        tickers, period=period, interval=interval,
        group_by="ticker", progress=False, auto_adjust=True, threads=True,
    )

    results = {}
    for ticker in tickers:
        try:
            df = raw[ticker].dropna()
            if len(df) > 50:
                results[ticker] = df
        except (KeyError, ValueError, TypeError):
            continue
    return results


def scan(tickers=None):
    return fetch_data(tickers or DEFAULT_TICKERS)
