import requests

def scrape_arbeitnow(keyword="python"):
    jobs = []
    page = 1
    max_pages = 3  # limit to avoid rate limiting

    try:
        while page <= max_pages:
            url = f"https://www.arbeitnow.com/api/job-board-api?page={page}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            for job in data.get("data", []):
                title = job.get("title", "")
                company = job.get("company", "")
                tags = job.get("tags", [])
                link = job.get("url", "")

                if keyword.lower() in title.lower() or any(keyword.lower() in tag.lower() for tag in tags):
                    jobs.append({
                        "title": title,
                        "company": company,
                        "link": link
                    })

            if not data.get("links", {}).get("next"):
                break
            page += 1

    except Exception as e:
        print(f"❌ Error fetching from Arbeitnow: {e}")

    return jobs

# Example test
if __name__ == "__main__":
    results = scrape_arbeitnow("python")
    for job in results[:5]:
        print(f"{job['title']} at {job['company']} → {job['link']}")
