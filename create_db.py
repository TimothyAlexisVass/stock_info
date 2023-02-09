import sqlite3

conn = sqlite3.connect("stock_info.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS company (
    ticker TEXT PRIMARY KEY,
    name TEXT,
    pe_ratio REAL,
    dividend REAL,
    earning_per_share REAL,
    target_price REAL,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS daily (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT,
    date DATE,
    price_open REAL,
    price_closed REAL,
    FOREIGN KEY (ticker) REFERENCES company(ticker) ON DELETE CASCADE,
    UNIQUE (ticker, date)
)
""")

conn.commit()
conn.close()
