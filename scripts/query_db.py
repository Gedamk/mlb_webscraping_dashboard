# query_db.py
# ---------------------------------
# Query MLB data from SQLite database and display insights.

import sqlite3
import pandas as pd
import os

DB_PATH = "data/mlb_data.db"

if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"Database not found: {DB_PATH}")

# Connect to the database
conn = sqlite3.connect(DB_PATH)

# ✅ Correct query for your current data structure
query = """
SELECT Year, Team, Runs
FROM mlb_events
ORDER BY Runs DESC
LIMIT 10;
"""

print("Running query...")
try:
    df = pd.read_sql_query(query, conn)
    print("Query executed successfully!\n")
    print(df)
except Exception as e:
    print(f"SQL query failed: {e}")
finally:
    conn.close()
