"""Daily trading-alert orchestrator. Runs once on startup, then every day at RUN_TIME."""
import os
import time
import traceback
from datetime import datetime

import pytz

from notifier import format_error, format_signals, send_telegram
from risk_engine import apply_risk
from scanner import DEFAULT_TICKERS, scan
from signal_engine import generate_signals

TIMEZONE = os.environ.get("TIMEZONE", "Europe/Istanbul")
RUN_TIME = os.environ.get("RUN_TIME", "10:00")  # 24h format
TICKERS_ENV = os.environ.get("TICKERS", "").strip()
TOP_N = int(os.environ.get("TOP_N", "3"))
MIN_SCORE = int(os.environ.get("MIN_SCORE", "50"))


def get_tickers():
    if TICKERS_ENV:
        return [t.strip().upper() for t in TICKERS_ENV.split(",") if t.strip()]
    return DEFAULT_TICKERS


def run_scan():
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M")
    print(f"\n[{now}] Scan started")

    try:
        tickers = get_tickers()
        print(f"[main] Scanning {len(tickers)} symbols")

        price_data = scan(tickers)
        print(f"[main] Got data for {len(price_data)} symbols")

        signals = generate_signals(price_data, min_score=MIN_SCORE)
        print(f"[main] {len(signals)} signals passed scoring")

        signals = apply_risk(signals)
        message = format_signals(signals, top_n=TOP_N)
        sent = send_telegram(message)
        print(f"[main] Done (telegram_sent={sent})")

    except Exception as e:
        err = f"{type(e).__name__}: {e}"
        print(f"[main] ERROR: {err}\n{traceback.format_exc()}")
        try:
            send_telegram(format_error(err))
        except Exception:
            pass


def main():
    tz = pytz.timezone(TIMEZONE)
    target_hour, target_minute = map(int, RUN_TIME.split(":"))

    print("=" * 50)
    print("Trading Alert System")
    print(f"Timezone:   {TIMEZONE}")
    print(f"Run time:   {RUN_TIME}  (daily)")
    print(f"Top N:      {TOP_N}")
    print(f"Min score:  {MIN_SCORE}")
    print("=" * 50)

    run_scan()
    last_run_date = datetime.now(tz).date()

    while True:
        now = datetime.now(tz)
        if last_run_date != now.date() and (now.hour, now.minute) >= (target_hour, target_minute):
            run_scan()
            last_run_date = now.date()
        time.sleep(30)


if __name__ == "__main__":
    main()
