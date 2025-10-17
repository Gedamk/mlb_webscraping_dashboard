import sqlite3, pandas as pd

conn = sqlite3.connect("data/mlb_data.db")
df = pd.read_csv("data/mlb_events_clean.csv")

df.to_sql("mlb_events", conn, if_exists="replace", index=False)
print("✅ Data imported into SQLite database!")
conn.close()
