# -*- coding: utf-8 -*-
"""
scripts/scrape_mlb.py
---------------------------------
Automated MLB History Scraper (Lesson 14 Project)
-------------------------------------------------
Uses Selenium + WebDriver Manager to extract baseball history data
from Baseball Reference (https://www.baseball-reference.com/)
and save results to CSV for later use in SQLite + Dashboard.
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def main():
    # =====================================================
    # ⚙️ Setup Chrome WebDriver with automatic manager
    # =====================================================
    options = Options()
    options.add_argument("--headless")  # Run in background (no browser UI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    print("🚀 Launching Chrome WebDriver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # =====================================================
        # 🌍 Target website
        # =====================================================
        url = "https://www.baseball-reference.com/leagues/majors/2023.shtml"
        print(f"🔗 Navigating to: {url}")
        driver.get(url)
        time.sleep(3)

        # =====================================================
        # 📊 Scrape example data table (Team stats by year)
        # =====================================================
        print("📦 Extracting data from table...")
        rows = driver.find_elements(By.CSS_SELECTOR, "table#teams_standard_batting tr")

        years, teams, runs = [], [], []

        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 5:
                years.append("2023")
                teams.append(cols[1].text)
                runs.append(cols[4].text)

        # =====================================================
        # 💾 Save to CSV
        # =====================================================
        df = pd.DataFrame({"Year": years, "Team": teams, "Runs": runs})
        output_path = "data/mlb_events.csv"

        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"✅ Data saved successfully to {output_path}")
        print(df.head())

    except Exception as e:
        print(f"❌ Error during scraping: {e}")

    finally:
        driver.quit()
        print("🧹 Browser closed. Scraping complete.")


if __name__ == "__main__":
    main()
