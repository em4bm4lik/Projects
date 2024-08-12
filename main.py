import requests
import re
import csv
from bs4 import BeautifulSoup
from pprint import pprint
from types import NoneType
from selenium import webdriver
from selenium.webdriver.common.by import By


class DataAppender:

    def append_data(self, url):

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title_element = soup.find("h1", class_="mt-0")
        title = title_element.text if title_element else 'Title not Found'

        phone_element = soup.find("a", href=re.compile('tel:'))
        phone = phone_element.text if phone_element else 'Phone Number not Found'

        site_element = soup.find("a", string='Visit Site')
        site = site_element.attrs['href'] if site_element else 'Website not Found'

        address_element = soup.find("address")
        address = address_element.text if address_element else 'Address not Found'

        directions_element = address_element.find_next_sibling(
            'a') if address_element else NoneType()

        directions = directions_element.attrs['href'] if directions_element else 'Link for Directions not Found'

        about_element = soup.find(class_='about_us')
        about = about_element.text if about_element else ''

        description_element = soup.find(class_='detailed_business_desc')
        description = description_element.text if description_element else ''

        services_heading_element = soup.find(
            "h2", string=re.compile('Services'))

        services_text_element = services_heading_element.find_next_sibling(
            "p") if services_heading_element else NoneType()

        services = services_heading_element.text + '\n' + \
            services_text_element.text if (
                services_heading_element and services_text_element) else ''

        with open('data.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([title, phone, site, address, directions,
                            about, description, services])


with open('data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Title ', 'Phone Number ', 'Website ', 'Address ',
                     'Link for Directions ', 'About ', 'Description ', 'Services '])

appender = DataAppender()

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
options.add_argument('start-maximized')

browser = webdriver.Chrome(options=options)
browser.get('https://botw.org/business/')

browser.find_element('link text', 'Last ›').send_keys('\n')
no_of_pages = int(browser.find_element('class name', 'page-item.active').text)

for i in range(1, no_of_pages + 1):
    browser.get('https://botw.org/business/'+str(i))

    links = browser.find_elements('link text', 'View Profile')

    for i in range(len(links)):
        links = browser.find_elements('link text', 'View Profile')
        links[i].send_keys('\n')
        appender.append_data(browser.current_url)
        browser.back()

browser.close()
