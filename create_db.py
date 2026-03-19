import sqlite3

# Veritabanı dosyası
DB_FILE = "bot.db"

# Bağlantı oluştur
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# sent_matches tablosu
cursor.execute("""
CREATE TABLE IF NOT EXISTS sent_matches (
    match_id TEXT PRIMARY KEY
)
""")

conn.commit()
conn.close()

print(f"{DB_FILE} başarıyla oluşturuldu ve tablo hazır!")
