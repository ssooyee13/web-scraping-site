from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


def extract_wwr_jobs(keyword):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    driver.get(f"{base_url}{keyword}")
    results = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = soup.find_all("section", class_="jobs")
    for job in jobs:
        job_posts = job.find_all('li')
        job_posts.pop(-1)
        for post in job_posts:
            anchors = post.find_all("a")
            anchor = anchors[1]
            link = anchor.get("href")
            company, kind, location = anchor.find_all("span", class_="company")
            title = anchor.find("span", class_="title")
            job_data = {
                'link': f"https://weworkremotely.com{link}",
                'company': company.string,
                'location': location.string,
                'position': title.string
            }
            results.append(job_data)
    return results
