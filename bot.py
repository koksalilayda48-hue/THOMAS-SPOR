import sqlite3
import requests
import threading
import time
import os
from telegram import Bot

# ---------------- AYARLAR (ENV) ----------------
TOKEN = os.getenv("BOT_TOKEN") or "8587288869:AAHA-giNXfRAkqHT7cLabVlVBEzinHq7qXg"
CHANNEL_ID = os.getenv("CHANNEL_ID") or "@thomasspororjinal"
API_KEY = os.getenv("API_KEY") or "VSE77SeYWYOWZVrPHgOoKqBJRXnPnU9y6oe4QcFdoEbSFGmgRi9xcRqG9iQp"

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

# ---------------- DB FONKSİYON ----------------
def is_sent(match_id):
    cursor.execute("SELECT 1 FROM sent_matches WHERE match_id=?", (match_id,))
    return cursor.fetchone() is not None

def save_match(match_id):
    cursor.execute("INSERT OR IGNORE INTO sent_matches (match_id) VALUES (?)", (match_id,))
    conn.commit()

# ---------------- API ----------------
def get_matches():
    try:
        r = requests.get(API_URL, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            print("API hata:", r.status_code)
            return []
        return r.json().get("response", [])
    except Exception as e:
        print("API exception:", e)
        return []

# ---------------- BOT LOOP ----------------
def run_bot():
    print("Bot loop başladı...")
    while True:
        matches = get_matches()

        for m in matches:
            try:
                match_id = str(m["fixture"]["id"])
                home = m["teams"]["home"]["name"]
                away = m["teams"]["away"]["name"]
                score = f"{m['goals']['home']} - {m['goals']['away']}"
                image = m["league"]["logo"]

                # Büyük takım filtresi
                if home not in BIG_TEAMS and away not in BIG_TEAMS:
                    continue

                # Tekrar kontrol
                if is_sent(match_id):
                    continue

                caption = f"{home} {score} {away}"

                # 🔥 SADE VE HATASIZ GÖNDERİM
                bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=image,
                    caption=caption
                )

                print("Gönderildi:", caption)
                save_match(match_id)

            except Exception as e:
                print("Maç işleme hata:", e)

        time.sleep(5)

# ---------------- BAŞLAT ----------------
if __name__ == "__main__":
    print("Bot aktif 🚀 FINAL SÜRÜM")
    threading.Thread(target=run_bot, daemon=True).start()

    while True:
        time.sleep(5)
