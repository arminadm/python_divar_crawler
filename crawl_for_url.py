import csv
import requests
from bs4 import BeautifulSoup

url = 'https://divar.ir/YOUR_ROUTE'
page = 1
ads = []
links = []
how_may_urls = 500

while len(links) < how_may_urls:
    params = {'page': page}
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    ads = soup.find_all('div', class_='post-card-item-af972')
    if not ads:
        print("#Nothing found!")
        break
    for ad in ads:
        try:
            ad_counter = len(links)
            if ad_counter == how_may_urls:
                break
            ad_link = ad.find('a')['href']
            links.append(f"https://divar.ir{ad_link}")
            print(f"# we found {ad_counter} items!")
        except:
            pass
    page += 1

with open('YOUR_URL_FILE_NAME.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for link in links:
        writer.writerow([link])