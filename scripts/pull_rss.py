import requests
import pandas as pd

SOURCES = {
    "remotive": "https://remotive.io/api/remote-jobs",
    "remoteok": "https://remoteok.com/api"
}

def pull_remotive():
    try:
        res = requests.get(SOURCES["remotive"])
        res.raise_for_status()  # Check for HTTP errors
        data = res.json().get("jobs", [])
        jobs = []
        for job in data:
            jobs.append({
                "job_title": job["title"],
                "company": job["company_name"],
                "original_url": job["url"],
                "platform": "remotive",
                "location": job["candidate_required_location"],
                "post_date": job["publication_date"]
            })
        return jobs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Remotive: {e}")
        return []
    except ValueError as e:
        print(f"Error decoding JSON for Remotive: {e}")
        return []

def pull_remoteok():
    try:
        res = requests.get(SOURCES["remoteok"], headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()  # Check for HTTP errors
        data = res.json()[1:]  # Skip metadata
        jobs = []
        for job in data:
            jobs.append({
                "job_title": job.get("position") or job.get("title"),
                "company": job.get("company"),
                "original_url": "https://remoteok.com" + job.get("url", ""),
                "platform": "remoteok",
                "location": job.get("location", ""),
                "post_date": job.get("date", "")
            })
        return jobs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from RemoteOK: {e}")
        return []
    except ValueError as e:
        print(f"Error decoding JSON for RemoteOK: {e}")
        return []

def save_csv(jobs):
    if jobs:
        df = pd.DataFrame(jobs)
        df.to_csv("output/rss_jobs.csv", index=False)
        print(f"✅ Saved {len(df)} jobs to output/rss_jobs.csv")
    else:
        print("No jobs to save.")

if __name__ == "__main__":
    all_jobs = pull_remotive() + pull_remoteok()
    save_csv(all_jobs)
