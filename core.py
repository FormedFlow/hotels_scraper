import requests
import re
import time
import csv
from bs4 import BeautifulSoup


def parse_hotel(link):
    hotel_r = requests.get(link)
    if not hotel_r.ok:
        return
    hotel_bs = BeautifulSoup(hotel_r.text, 'lxml')

    print(f'{link} before getting meta tags')
    temp = {}
    temp['Brand'] = hotel_bs.find('meta', attrs={'name': 'X-accor-brand-label'})['content']
    temp['Name'] = hotel_bs.find('meta', attrs={'name': 'X-accor-brand-label'})['content']
    temp['Address'] = hotel_bs.find('div', class_='infos__content').p.text
    temp['Url'] = link
    print(temp)
    return temp


# name, brand, address, url


hotels = []
target_url = 'https://all.accor.com/de/country/hotels-deutschland-pde.shtml'
r = requests.get(target_url)
bs = BeautifulSoup(r.text, 'lxml')

regions = bs.find_all('a', href=re.compile('^https://all.accor.com/de/region'))

# for region in regions:
for region in regions[1:]:
    time.sleep(10)
    region_r = requests.get(region['href'])
    region_bs = BeautifulSoup(region_r.text, 'lxml')
    direct_links = region_bs.find_all('a', href=re.compile('^https://all.accor.com/hotel/'))
    if direct_links:
        for link in direct_links:
            time.sleep(1)
            result = parse_hotel(link['href'])
            if result and result not in hotels:
                hotels.append(result)

    city_links = region_bs.find_all('a', href=re.compile('^https://all.accor.com/de/city/hotels'))
    if city_links:
        for link in city_links:
            time.sleep(1)
            city_r = requests.get(link['href'])
            city_bs = BeautifulSoup(city_r.text, 'lxml')
            hotel_links = city_bs.find_all('a', href=re.compile('^https://all.accor.com/hotel/'))
            for hotel_link in hotel_links:
                time.sleep(1)
                result = parse_hotel(hotel_link['href'])
                if result and result not in hotels:
                    hotels.append(result)


with open('hotels.csv', 'a', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=hotels[0].keys())
    writer.writerows(hotels)
