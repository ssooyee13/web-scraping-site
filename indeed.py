from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests


def get_page_count(keyword):
    base_url = "https://kr.indeed.com/jobs?q="
    driver = requests.get(f"{base_url}{keyword}")
    if driver.status_code == 400:
        print("Can't request page")
    else:
        soup = BeautifulSoup(driver.text, "html.parser")
        pagination = soup.find("nav", class_="pagination-list")
        if pagination == None:
            return 1
        pages = pagination.find_all("div", recursive=False)
        count = (len(pages))
        if count >= 5:
            return 5
        else:
            return count
    print(get_page_count("python"))
    print(get_page_count("nextjs"))
    print(get_page_count("django"))
    print(get_page_count("nestjs"))


def extract_indeed_jobs(keyword):
    results = []
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs"
        final_url = (f"{base_url}?q={keyword}&start={page*10}")
        print("requesting", final_url)
        driver = webdriver.Chrome()
        driver.get(final_url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        jobs_list = soup.find("ul", class_="css-zu9cdh eu4oa1w0")
        jobs = jobs_list.find_all("li", recursive=False)

        for job in jobs:
            zone = job.find('div', class_="mosaic-zone")
            if zone is None:
                anchor = job.select("h2 a")
                title = anchor[0]['aria-label']
                link = anchor[0]['href']
                company = job.find('span', class_='css-1x7z1ps eu4oa1w0')
                location = job.find('div', class_="css-t4u72d eu4oa1w0")
                job_data = {
                    'link': f"https: //kr.indeed.com{link}",
                    'company': company.string.replace(",", " "),
                    'location': location.string,
                    'position': title,
                }
                results.append(job_data)
                driver.quit()
    return results
