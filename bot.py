import sqlite3
import requests
import threading
import time
from telegram import Bot

# ---------------- AYARLAR ----------------
TOKEN = "8587288869:AAHA-giNXfRAkqHT7cLabVlVBEzinHq7qXg"            # Buraya bot token
CHANNEL_ID = "@thomasspororjinal" # Kanal kullanıcı adı
API_KEY = "VSE77SeYWYOWZVrPHgOoKqBJRXnPnU9y6oe4QcFdoEbSFGmgRi9xcRqG9iQp"  # API-Football key

bot = Bot(token=TOKEN)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS sent_matches (
    match_id TEXT PRIMARY KEY
)
""")
conn.commit()

# ---------------- TAKIMLAR ----------------
BIG_TEAMS = [
    "Fenerbahçe", "Galatasaray", "Beşiktaş",
    "Manchester United", "Liverpool", "Chelsea", "Arsenal", "Manchester City",
    "Real Madrid", "Barcelona", "Atletico Madrid",
    "Bayern Munich", "Borussia Dortmund",
    "Juventus", "AC Milan", "Inter",
    "PSG", "Lyon", "Marseille"
]

# ---------------- API ----------------
API_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# ---------------- DATABASE FONKSİYONLARI ----------------
def is_sent(match_id):
    cursor.execute("SELECT 1 FROM sent_matches WHERE match_id=?", (match_id,))
    return cursor.fetchone() is not None

def save_match(match_id):
    cursor.execute("INSERT INTO sent_matches (match_id) VALUES (?)", (match_id,))
    conn.commit()

# ---------------- MAÇ ÇEKME ----------------
def get_matches():
    try:
        r = requests.get(API_URL, headers=HEADERS)
        if r.status_code != 200:
            print("API hata:", r.status_code)
            return []
        data = r.json()
        return data.get("response", [])
    except Exception as e:
        print("API exception:", e)
        return []

# ---------------- BOT LOOP ----------------
def run_bot():
    while True:
        matches = get_matches()
        for m in matches:
            match_id = str(m["fixture"]["id"])
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            score = f"{m['goals']['home']} - {m['goals']['away']}"
            image = m["league"]["logo"]

            # Sadece büyük takımlar
            if home not in BIG_TEAMS and away not in BIG_TEAMS:
                continue

            # Tekrar kontrol
            if is_sent(match_id):
                continue

            caption = f"{home} {score} {away}"

            try:
                bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=image,
                    caption=caption
                )
                print("Gönderildi:", caption)
                save_match(match_id)
            except Exception as e:
                print("Telegram hata:", e)

        time.sleep(5)  # 5 saniyede bir kontrol

# ---------------- BAŞLAT ----------------
if __name__ == "__main__":
    print("Bot aktif 🚀 (Gelişmiş SQLite sürümü)")
    threading.Thread(target=run_bot, daemon=True).start()
    while True:
        time.sleep(3)
