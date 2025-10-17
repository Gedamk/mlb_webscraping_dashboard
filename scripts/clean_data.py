# -*- coding: utf-8 -*-
"""
scripts/clean_data.py
---------------------------------
Clean and transform MLB event data before database import.
Reads data/mlb_events.csv and outputs data/mlb_events_clean.csv
"""

import pandas as pd
import os

# =====================================================
# Load the raw CSV
# =====================================================
input_path = "data/mlb_events.csv"
output_path = "data/mlb_events_clean.csv"

if not os.path.exists(input_path):
    raise FileNotFoundError(f"❌ File not found: {input_path}")

print(f"Loading data from {input_path}...")
df = pd.read_csv(input_path)

print(f"Columns found: {list(df.columns)}")

# =====================================================
#  Clean + Transform Data
# =====================================================
# Rename columns safely (normalize column names)
df.columns = [col.strip().title() for col in df.columns]

# Clean string data
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].astype(str).str.strip().str.title()

# Convert numeric columns
if "Runs" in df.columns:
    df["Runs"] = pd.to_numeric(df["Runs"], errors="coerce").fillna(0).astype(int)

# Drop duplicates and NaNs
df.drop_duplicates(inplace=True)
df.dropna(how="all", inplace=True)

# =====================================================
#  Save Clean Data
# =====================================================
os.makedirs("data", exist_ok=True)
df.to_csv(output_path, index=False, encoding="utf-8")

print(f" Clean data saved to {output_path}")
print(df.head())
