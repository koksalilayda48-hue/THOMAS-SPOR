import json
import requests
import threading
import time
import os
from telegram import Bot

# 🔐 Güvenli kullanım (istersen .env kullanabilirsin)
TOKEN = "BOT_TOKENINI_BURAYA_YAZ"
CHANNEL_ID = "@thomasspororjinal"
API_KEY = "VSE77SeYWYOWZVrPHgOoKqBJRXnPnU9y6oe4QcFdoEbSFGmgRi9xcRqG9iQp"

bot = Bot(token=TOKEN)

# Gönderilen maçları sakla
try:
    with open("sent.json", "r") as f:
        sent = set(json.load(f))
except:
    sent = set()

# Büyük takımlar
BIG_TEAMS = [
    "Fenerbahçe", "Galatasaray", "Beşiktaş",
    "Manchester United", "Liverpool", "Chelsea", "Arsenal", "Manchester City",
    "Real Madrid", "Barcelona", "Atletico Madrid",
    "Bayern Munich", "Borussia Dortmund",
    "Juventus", "AC Milan", "Inter",
    "PSG"
]

API_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def get_matches():
    try:
        r = requests.get(API_URL, headers=HEADERS)
        if r.status_code != 200:
            print("API hata:", r.status_code)
            return []
        data = r.json()
        return data.get("response", [])
    except Exception as e:
        print("API hata:", e)
        return []

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

            # Tekrar kontrolü
            if match_id in sent:
                continue

            caption = f"{home} {score} {away}"

            try:
                bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=image,
                    caption=caption
                )
                print("Gönderildi:", caption)
                sent.add(match_id)
            except Exception as e:
                print("Telegram hata:", e)

        # Kaydet
        with open("sent.json", "w") as f:
            json.dump(list(sent), f)

        time.sleep(5)  # 5 saniye

# Başlat
if __name__ == "__main__":
    print("Bot aktif 🚀")
    threading.Thread(target=run_bot).start()

    while True:
        time.sleep(5)
