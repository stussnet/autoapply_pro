from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def scrape_remoteok(keyword="python"):
    jobs = []

    chrome_options = Options()
    # Comment out headless mode so you can SEE what's going on
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = f"https://remoteok.com/remote-{keyword}-jobs"
        print(f"Navigating to {url}")
        driver.get(url)

        time.sleep(5)  # give page time to load

        job_rows = driver.find_elements(By.XPATH, "//tr[@data-id]")
        print(f"Found {len(job_rows)} job rows")

        for row in job_rows:
            try:
                title_elem = row.find_element(By.TAG_NAME, "h2")
                company_elem = row.find_element(By.TAG_NAME, "h3")
                link_elem = row.find_element(By.CLASS_NAME, "preventLink")

                job = {
                    "title": title_elem.text.strip() if title_elem else "N/A",
                    "company": company_elem.text.strip() if company_elem else "N/A",
                    "link": "https://remoteok.com" + link_elem.get_attribute("href") if link_elem else "N/A"
                }
                print(f"✔️ {job['title']} at {job['company']} – {job['link']}")
                jobs.append(job)
            except Exception as e:
                print(f"❌ Error parsing job row: {e}")
                continue
    except Exception as e:
        print(f"🚨 Failed to load or extract: {e}")
    finally:
        driver.quit()

    return jobs

# Run this file directly to test:
if __name__ == "__main__":
    result = scrape_remoteok("python")
    print(f"Total jobs found: {len(result)}")
