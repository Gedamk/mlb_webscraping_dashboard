import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# =====================================================
# 🏠 Dashboard Title
# =====================================================
st.set_page_config(page_title="MLB History Dashboard", layout="wide")
st.title("⚾ MLB History Dashboard")
st.markdown("Explore team performance data scraped, cleaned, and stored in SQLite.")

# =====================================================
# 📂 Load Data
# =====================================================
conn = sqlite3.connect("data/mlb_data.db")
df = pd.read_sql_query("SELECT * FROM mlb_events", conn)
conn.close()

# Ensure correct data types
df["Year"] = df["Year"].astype(int)

# =====================================================
# 🔍 Filter by Year
# =====================================================
year = st.selectbox("Select Year:", sorted(df["Year"].unique(), reverse=True))
filtered = df[df["Year"] == year]

# =====================================================
# 📊 Data Preview
# =====================================================
st.subheader(f"Team Performance for {year}")
st.dataframe(filtered)

# =====================================================
# 📈 Visualization 1 — Bar Chart (Top Teams by Runs)
# =====================================================
st.subheader(f"Top 10 Teams by Runs - {year}")

fig_bar = px.bar(
    filtered.sort_values("Runs", ascending=False).head(10),
    x="Team",
    y="Runs",
    text="Runs",
    title=f"Top 10 Teams by Runs - {year}",
    color="Runs",
    color_continuous_scale="blues",
    template="plotly_white"
)
fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
fig_bar.update_layout(xaxis_title="Team", yaxis_title="Runs", showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)

# =====================================================
# 📈 Visualization 2 — Line Chart (Runs Over Time)
# =====================================================
st.subheader("Total Runs by Year")

yearly_runs = df.groupby("Year")["Runs"].sum().reset_index()
fig_line = px.line(
    yearly_runs,
    x="Year",
    y="Runs",
    markers=True,
    title="Total Runs by Year",
    template="plotly_dark"
)
st.plotly_chart(fig_line, use_container_width=True)

# =====================================================
# 🧮 Summary Stats
# =====================================================
st.subheader("Summary Statistics")
st.write(df.describe())
