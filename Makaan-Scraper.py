import requests
from bs4 import BeautifulSoup
import smtplib
import time
import csv
import numpy as np
import pandas as pd
import regex as re

# User Agent
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

# Getting random proxy

def getRandomProxy():
    proxy = {
    "http": f"http://scraperapi:APIKey@proxy-server.scraperapi.com:8001",
    "https": f"http://scraperapi:APIKey@proxy-server.scraperapi.com:8001"}

    return proxy
    

# Getting html page content for testing bs4 functions

def getContent():
    # URL = input('Enter 99acres Property URL: ')
    urls = []
    for i in range(1):

        URL = "https://www.makaan.com/bangalore-property/indira-nagar-flats-for-sale-50162?page=3"
        page = requests.get(URL, proxies=getRandomProxy(), headers=headers, verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')

    with open('Thane_East.txt', 'w', encoding='utf-8') as file:
        file.write(str(soup) + ', ')


# Getting list of links from which the data is needs to be extracted

def getLinks():
    # URL = input('Enter 99acres Property URL: ')
    urls = []
    for i in range(20):

        URL = "https://www.makaan.com/delhi-property/paschim-vihar-flats-for-sale-51808?page={}".format(i+1)
        page = requests.get(URL, proxies=getRandomProxy(), verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')

        for span_tag in soup.find_all('span', attrs={'data-url': True}):
            urls.append(span_tag['data-url'])

    for i in list(set(urls)):
        print(i)

    with open('All_cities_linktxt/paschim.txt', 'w') as file:
        for item in list(set(urls)):
            file.write(str(item) + ', ')



# Opening file which contains list of links which was created by function getLinks()

with open('All_cities_linktxt/paschim.txt', 'r') as file:
    links = file.read()

link_lst = [i.strip() for i in links.split(',')]
link_lst.remove("/download-mobileapp")
link_lst.remove("")
link_lst = link_lst[:250]



def getDetails(link_list):
    link_list = link_list
    main_list = []
    for i in link_list:
        
        url = str(i).strip()
        page = requests.get(url, proxies=getRandomProxy(), verify=False, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
            
        try:
            title = soup.title.text
        except:
            title = np.nan

        try:
            type = soup.find('span',{'class':'type'}).text
        except:
            type = np.nan

        try:
            floorsize = soup.find('span', itemprop = 'floorSize').text
        except:
            floorsize = np.nan

        try:
            carpet_area = soup.find('td',{'id':'Carpet area'}).text
        except:
            carpet_area = np.nan

        try:
            price_per_sqft  = soup.find('div',{'class':'rate-wrap'}).text.strip()
        except:
            price_per_sqft = np.nan

        try:
            price = soup.find('meta', itemprop='price').get('content')
        except:
            price = np.nan

        try:
            status = soup.find_all('td', id = "Status")[0].text.strip()
        except:
            status = np.nan

        try:
            no_bathroom = soup.find('td',id='Bathrooms').get('title')
        except:
            no_bathroom = np.nan

        try:
            is_new = soup.find('td',id='New/Resale').get('title')
        except:
            is_new = np.nan

        try:
            description = soup.find('div', {'class': 'clearfix hidden'}).text.strip()
        except:
            description = np.nan

        try:
            facing = soup.find('td', {'id': 'Facing'}).text.strip()
        except:
            facing = np.nan

        try:
            furnishing_status = soup.find_all('td', id = "Status")[1].text.strip()
        except:
            furnishing_status = np.nan

        try:
            locality = soup.find('span', itemprop = 'addressLocality').text
        except:
            locality = np.nan
            
        try:
            about_locality = soup.find('div', {'class': 'locality-wrap'}).text.strip()
        except:
            about_locality = np.nan

        try:
            feature_lst = []
            for i in range(len(soup.find_all('div',{'class': 'outside-container'}))):
                main_html = soup.find_all('div',{'class': 'outside-container'})
                internal_ele = BeautifulSoup(str(main_html[i]), 'html.parser')
                    # try:
                    #     if not re.search('<div class="overlay"></div>', str(internal_ele)):
                    #         amenity = internal_ele.find('div',{'itemprop': 'amenityFeature'}).text.strip()
                    # except:
                    #     amenity = None

                try:
                    if not re.search('<div class="overlay"></div>', str(internal_ele)):
                        feature = internal_ele.find('div',{'class':'txt'}).text.strip()
                except:
                    feature = None
                    
                feature_lst.append(feature)

            amenities = str(list(set(feature_lst)))
            
        except:
            amenities = np.nan
            
        main_dict = {'URL': str(url), 'Title': title, 'Type': type, 'Floorsize': floorsize, 'Carpet_area': carpet_area, 'Price_per_sqft': price_per_sqft,
                        'Price': price, 'Status': status,'No_Of_Bathrooms': no_bathroom, 'Is_new': is_new, 'Description': description, 'Facing': facing,               
                        'Furnishing_status': furnishing_status,'Locality':locality, 'About_locality':about_locality, 'Amenities_list': amenities}
            
        main_list.append(main_dict)
        
    df_main = pd.DataFrame(main_list)
    df_main.to_csv('All_cities_csv/paschim.csv')
    return print(df_main)

getDetails(link_lst)

# getContent()

# getLinks()

# print(len(link_lst))
# print(link_lst)




