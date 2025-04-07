import requests

def scrape_remotive(keyword="python"):
    jobs = []
    url = f"https://remotive.io/api/remote-jobs?search={keyword}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        for job in data.get("jobs", []):
            jobs.append({
                "title": job.get("title", "N/A"),
                "company": job.get("company_name", "N/A"),
                "link": job.get("url", "#")
            })

    except Exception as e:
        print(f"❌ Error fetching jobs from Remotive API: {e}")

    return jobs

# Example usage
if __name__ == "__main__":
    results = scrape_remotive("python")
    for job in results[:5]:
        print(f"{job['title']} at {job['company']} → {job['link']}")
