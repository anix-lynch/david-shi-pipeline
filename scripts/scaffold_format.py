import pandas as pd

REQUIRED_COLUMNS = [
    "job_title", "company", "original_url", "poster_name", "poster_linkedin",
    "poster_title", "poster_type", "confidence", "reason",
    "meta_scrape_status", "org_search_status",
    "poster_email", "poster_phone", "poster_twitter", "poster_github",
    "contact_source"
]

def validate_scaffold(filepath):
    df = pd.read_csv(filepath)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        print(f"❌ Missing columns: {missing}")
        return
    print(f"✅ {filepath} passed scaffold validation.")
    print(f"🔢 Rows: {len(df)}")
    print(df.head(1).T)

if __name__ == "__main__":
    validate_scaffold("data/david_shi_scaffold_format.csv")
