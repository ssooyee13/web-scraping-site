from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_page_count(keyword):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome()
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", class_="css-jbuxu0 ecydgvn0")
    if pagination == None:
        return 1
    pages = pagination.find_all(
        "div", recursive=False, class_="css-tvvxwd ecydgvn1")
    count = (len(pages))
    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=options)
    results = []
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs"
        final_url = (f"{base_url}?q={keyword}&start={page*10}")
        browser.get(final_url)
        print("requesting", final_url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
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
                    'link': f"https://kr.indeed.com{link}",
                    'company': company.string.replace(",", " "),
                    'location': location.string,
                    'position': title
                }
                results.append(job_data)
        browser.quit()
    print("complete")
    return results
