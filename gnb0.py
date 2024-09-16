import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.getonbrd.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

jobs = []
job_cards = soup.find_all("a", class_="gb-results-list__item")

for job in job_cards:
    title_element = job.find("h4", class_="gb-results-list__title").find("strong")
    title = title_element.text.strip() if title_element else "Título no disponible"

    company_element = job.find("div", class_="size0").find("strong")
    company = company_element.text.strip() if company_element else "Compañía no disponible"

    location_element = job.find("span", class_="location")
    if location_element:
        location_text = location_element.get_text(separator="\n", strip=True)
        location = location_text.split('\n')[0].strip() if location_text else "Ubicación no disponible"
    else:
        location = "Ubicación no disponible"

    details_url = job['href']
    if details_url:
        if not details_url.startswith("http"):
            details_url = "https://www.getonbrd.com" + details_url

        details_response = requests.get(details_url)

        details_response = requests.get(details_url)
        details_soup = BeautifulSoup(details_response.content, "html.parser")

        job_body_element = details_soup.find("div", id="job-body")
        if job_body_element:
            description_parts = job_body_element.find_all("div", class_="gb-rich-txt")
            description = "\n\n".join([part.get_text(strip=True) for part in description_parts])
        else:
            description = "Descripción no disponible"
    else:
        description = "Enlace de detalles no disponible"

    jobs.append({
        "Título": title,
        "Compañía": company,
        "Ubicación": location,
        "Descripción": description
    })

df = pd.DataFrame(jobs)
df.to_csv("trabajos.csv", index=False)
print("Datos exportados a trabajos.csv")
