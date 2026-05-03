"""Send Telegram messages and format trade alerts."""
import html
import os

import requests

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def send_telegram(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[notifier] TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID missing — printing message:")
        print(message)
        return False

    try:
        r = requests.post(
            TELEGRAM_API.format(token=token),
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=15,
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[notifier] failed: {e}")
        return False


def format_signals(signals, top_n=3):
    if not signals:
        return (
            "📊 <b>Günlük Tarama</b>\n\n"
            "Bugün için kriterleri karşılayan işlem fırsatı bulunmadı.\n"
            "Yarın tekrar kontrol edilecek."
        )

    lines = ["📊 <b>Günlük Top İşlem Fırsatları</b>\n"]
    for i, s in enumerate(signals[:top_n], 1):
        reasons = " • ".join(html.escape(r) for r in s["reasons"])
        lines.append(
            f"<b>{i}. {html.escape(s['ticker'])}</b>  |  Skor: {s['score']}/100\n"
            f"💰 Giriş: <b>{s['entry']:.2f}</b>\n"
            f"🛑 Stop: {s['stop_loss']:.2f}  ({s['stop_pct']:.1f}%)\n"
            f"🎯 Hedef: {s['take_profit']:.2f}  (+{s['target_pct']:.1f}%)\n"
            f"📈 R/R: 1:{s['risk_reward']:.1f}\n"
            f"📊 RSI: {s['rsi']:.1f}\n"
            f"<i>{reasons}</i>\n"
        )
    lines.append("\n⚠️ Yatırım tavsiyesi değildir. Kendi araştırmanızı yapın.")
    return "\n".join(lines)


def format_error(error_msg):
    return (
        "⚠️ <b>Tarayıcı Hatası</b>\n\n"
        f"{html.escape(str(error_msg))}\n\n"
        "Bir sonraki çalıştırmada tekrar denenecek."
    )
