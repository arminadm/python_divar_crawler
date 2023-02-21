import requests
from bs4 import BeautifulSoup
import openpyxl
import csv
from time import sleep


def main():
    counter = 0
    failed_case = 0
    success_case = 0
    # open the CSV file
    with open('your_url_file.csv', newline='') as csvfile:
        # create a CSV reader object
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        # iterate over the rows in the CSV file
        for url in reader:
            # wait 5 seconds before sending request for next url
            sleep(1)
            print("#")
            sleep(1)
            print("##")
            sleep(1)
            print("###")

            # process the row data
            print(f"{counter}-{url[0]}")
            try:
                status = crawl_details(url[0])
            except:
                status = False

            # printing logs
            if status == False:
                failed_case += 1
                print("Failed")
            else:
                print("Success")
                success_case += 1
            print("===================================")
            counter += 1
    
    print("##########################")
    print(f"total records: {counter}")
    print(f"failed records: {failed_case}")
    print(f"success records: {success_case}")


def crawl_details(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Response error: {response.status_code}")
        return False
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('div',  class_='kt-page-title__title kt-page-title__title--responsive-sized').text.strip().replace('\u200c', ' ')
    about = soup.find('div',  class_='kt-page-title__subtitle kt-page-title__subtitle--responsive-sized').text.strip().replace('\u200c', ' ')
    head_params = soup.find_all('div',  class_='kt-group-row-item kt-group-row-item--info-row')
    body_params = soup.find_all('div',  class_='kt-base-row kt-base-row--large kt-unexpandable-row')
    description = soup.find('p', class_='kt-description-row__text kt-description-row__text--primary').text.strip().replace('\u200c', ' ')
    description = description.replace('\n', ';')
    related_url = url

    answer = []

    answer.append(f"title: {title}")

    time, loc = about.split('در')
    answer.append(f"time: {time}")
    answer.append(f"loc: {loc}")

    for param in head_params:
        try:
            k = param.find('span', class_='kt-group-row-item__title kt-body kt-body--sm').text.replace('\u200c', ' ')
        except:
            k = "Null"

        try:
            v = param.find('span', class_='kt-group-row-item__value').text.replace('\u200c', ' ')
        except:
            v = "Null"
        answer.append(f"{k}: {v}")

    for param in body_params:
        try:
            k = param.find('div', class_='kt-base-row__start kt-unexpandable-row__title-box').text.replace('\u200c', ' ')
        except:
            k = "Null"

        try:
            v = param.find('div', class_='kt-base-row__end kt-unexpandable-row__value-box').text.replace('\u200c', ' ')
        except:
            v = "Null"
        answer.append(f"{k}: {v}")

    answer.append(f"description: {description}")
    answer.append(f"related_link: {related_url}")

    # add data to excel
    worksheet.append(answer)

    return True


if __name__ == '__main__':
    # create a new workbook object
    workbook = openpyxl.Workbook()

    # select the active worksheet
    worksheet = workbook.active

    # start the main progress
    main()

    # save the result    
    workbook.save('output.xlsx')
