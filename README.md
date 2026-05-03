# Borsa Alert — Daily Trading Signals to Telegram

Tarar BIST hisselerini → en iyi 3 fırsatı seçer → Telegram'a yollar. Her gün otomatik.

---

## ⚡ HIZLI KURULUM (15 dakika)

### 1) Telegram Bot oluştur

1. Telegram'da **@BotFather**'a yaz → `/newbot` → bota isim ver.
2. BotFather sana bir **token** verir (örn: `7891234567:AAH...`). **Kopyala.**
3. **@userinfobot**'a `/start` yaz → sana **chat ID**'ni verir (örn: `123456789`). **Kopyala.**
4. **Kendi botuna `/start` yaz** (zorunlu — yoksa bot sana mesaj atamaz).

### 2) Kodu GitHub'a yükle (tek seferlik)

> Railway, kodu GitHub'dan çeker. Komut satırı yok — sürükle-bırak.

1. [github.com](https://github.com) → kayıt ol (ücretsiz).
2. Sağ üst **+** → **New repository** → adı: `borsa-alert` → **Create**.
3. Açılan sayfada **uploading an existing file** linkine tıkla.
4. Bu klasördeki **TÜM dosyaları** sürükle-bırak (`.env` HARİÇ — varsa atma).
5. Aşağıda **Commit changes** → tıkla.

### 3) Railway'e deploy et

1. [railway.app](https://railway.app) → **Login with GitHub**.
2. **New Project** → **Deploy from GitHub repo** → `borsa-alert` seç.
3. Railway otomatik build başlatır. Hemen üstüne tıkla → **Variables** sekmesi.
4. **+ New Variable** ile şunları ekle:

   | Name                  | Value                       |
   | --------------------- | --------------------------- |
   | `TELEGRAM_BOT_TOKEN`  | (BotFather token'ı)         |
   | `TELEGRAM_CHAT_ID`    | (userinfobot chat ID)       |

5. Otomatik yeniden deploy olur. **Deployments** sekmesinden logları görebilirsin.
6. Birkaç saniye içinde Telegram'a ilk mesaj düşer ✅

### 4) Bitti

Her gün saat **10:00 (TR)** otomatik tarama → Telegram bildirimi.

---

## 🔧 İSTEĞE BAĞLI AYARLAR

Railway → Variables sekmesinden değiştir:

| Değişken           | Default            | Açıklama                                          |
| ------------------ | ------------------ | ------------------------------------------------- |
| `RUN_TIME`         | `10:00`            | Günlük çalışma saati (24h, TR saati)              |
| `TIMEZONE`         | `Europe/Istanbul`  | Saat dilimi                                       |
| `TOP_N`            | `3`                | Kaç fırsat gönderilsin                            |
| `MIN_SCORE`        | `50`               | Minimum sinyal skoru (0-100)                      |
| `TICKERS`          | (BIST 30)          | Virgüllü liste — örn `AAPL,MSFT,NVDA` (US için)   |

---

## 🧠 NASIL ÇALIŞIYOR

Her hisse 5 kriterde puanlanır (toplam 100):

- **Trend** — fiyat 50 günlük EMA'nın üstünde mi (+25)
- **Momentum** — EMA20 > EMA50 mı (+20)
- **RSI** — 50-70 arası mı (güçlü, +25) veya 40-50 (nötr, +10)
- **Hacim** — 20 günlük ortalamanın üstünde mi (+15)
- **Kırılım** — 20 günlük zirveye yakın mı (+15)

Stop loss = **giriş − 2×ATR** (volatiliteye göre).
Hedef = **risk × 2** (1:2 R/R).

---

## 🧪 LOKAL TEST (opsiyonel)

```bash
pip install -r requirements.txt
# .env dosyası oluştur (.env.example'ı kopyala, kendi değerlerini gir)
python main.py
```

---

## ⚠️ UYARI

Bu sistem yatırım tavsiyesi vermez. Sadece teknik analiz tabanlı bir tarayıcıdır.
Tüm yatırım kararlarını kendi sorumluluğunda ver.
