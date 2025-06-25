import pandas as pd
from pathlib import Path

INPUT_PATH = Path("output/rss_jobs.csv")
OUTPUT_PATH = Path("output/rss_jobs_scaffold.csv")

def convert_to_scaffold(df):
    scaffold = pd.DataFrame({
        "job_title": df["job_title"],
        "company": df["company"],
        "original_url": df["original_url"],
        "poster_name": "",
        "poster_linkedin": "",
        "poster_title": "",
        "poster_type": "",
        "confidence": "",
        "reason": "",
        "meta_scrape_status": "",
        "org_search_status": "",
        "poster_email": "",
        "poster_phone": "",
        "poster_twitter": "",
        "poster_github": "",
        "contact_source": ""
    })
    return scaffold

def main():
    if not INPUT_PATH.exists():
        print("❌ rss_jobs.csv not found.")
        return

    df = pd.read_csv(INPUT_PATH)
    scaffold = convert_to_scaffold(df)
    scaffold.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Scaffold created: {OUTPUT_PATH} with {len(scaffold)} rows.")

if __name__ == "__main__":
    main()
