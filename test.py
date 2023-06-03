import requests
from bs4 import BeautifulSoup
import smtplib
import time
import csv
import numpy as np
import regex as re

main_text = """<h2 title="Amenities">Amenities</h2><div class="m-scroll-wrap"><div class="icons-list js-list js-mobscroll" data-type="list"><div class="listitem js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-intercom"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span><span class="path9"></span><span class="path10"></span><span class="path11"></span><span class="path12"></span><span class="path13"></span><span class="path14"></span></span></div><div class="txt" itemprop="amenityFeature">Intercom</div></div></div><div class="listitem js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-power"><span class="path1"></span><span class="path2"></span><span class="path3"></span></span></div><div class="txt" itemprop="amenityFeature">Full Power Backup</div></div></div><div class="listitem js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-lift"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span></span></div><div class="txt" itemprop="amenityFeature">Lift(s)</div></div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-children"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span><span class="path9"></span><span class="path10"></span><span class="path11"></span><span class="path12"></span><span class="path13"></span></span></div><div class="txt" itemprop="amenityFeature">Children's play area</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-club-house"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span></span></div><div class="txt" itemprop="amenityFeature">Club House</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-garden"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span><span class="path9"></span></span></div><div class="txt" itemprop="amenityFeature">Landscaped Gardens</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-swimming-pool"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span></span></div><div class="txt" itemprop="amenityFeature">Swimming Pool</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-football"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span><span class="path9"></span><span class="path10"></span><span class="path11"></span><span class="path12"></span></span></div><div class="txt" itemprop="amenityFeature">Sports Facility</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-jogging-track"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span></span></div><div class="txt" itemprop="amenityFeature">Jogging Track</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-security"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span></span></div><div class="txt" itemprop="amenityFeature">24 X 7 Security</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><i class="icon-gym"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span></i></div><div class="txt" itemprop="amenityFeature">Gymnasium</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div></div></div></div><div class="furnishings-wrap js-list-wrap" data-module="divExpansion"><script type="text/x-config">{"category":"FURNISHINGS_MODULE"}</script><h3>Furnishings</h3><div class="m-scroll-wrap"><div class="icons-list js-list js-mobscroll" data-type="list"><div class="listitem js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-fire"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span></span></div><div class="txt">Gas connection</div></div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-ac"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span><span class="path9"></span><span class="path10"></span></span></div><div class="txt">AC</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-wardrobe"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span><span class="path9"></span><span class="path10"></span></span></div><div class="txt">Wardrobe</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-TV"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span></span></div><div class="txt">TV</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-fridge"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span></span></div><div class="txt">Refrigerator</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-sofa"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span></span></div><div class="txt">Sofa</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-wifi"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span></span></div><div class="txt">Wifi</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-dining-table"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span><span class="path9"></span><span class="path10"></span><span class="path11"></span><span class="path12"></span></span></div><div class="txt">Dining Table</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div><div class="listitem disabled js-moblist-item"><div class="outside-container"><div class="icon-wrap"><span class="icon-bed"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span><span class="path6"></span><span class="path7"></span><span class="path8"></span><span class="path9"></span></span></div><div class="txt">BED</div><div class="overlay"></div></div><div class="notPresent">Not Available</div></div></div></div></div><section class="ra_banner" style="margin-bottom: 20px;"><a href="https://housing.com/edge/rent-agreement?source-makaan-iq" rel="noopener noreferrer" target="_blank"><img alt="Rent Agreement" data-src="//static.makaan.com/images/ra_hook/RA_Banner_Details_Desktop.93e32441.png" object-fit="contain" src="//static.makaan.com/images/dummyPX.e679fbd4.png" style="width: calc(100%);"/></a></section><div class="tmp-btn-wrap"><a class="cbtn cbtn-p" data-bhk="2" data-budget="23000000" data-call-now="" data-cityid="18" data-companyid="100107487" data-companyimage="https://static.makaan.com/11/100107487/289/105027054.jpeg?width=130&amp;height=100" data-companyname="Veda Realty" data-companytype="Broker" data-companyuserid="101292916" data-listingcategory="Primary" data-listingid="16253173" data-listingimage="https://static.makaan.com/17/16253173/287/120287341.jpeg?width=1024&amp;height=576" data-localityid="50043" data-projectid="750619" data-propertytype="Apartment" data-propertytypeid="1" data-type="connect-now">request more details</a></div></div><div class="info-card loc-bui-wrap"><div class="sleek-tabs clearfix" data-module="tabs" id="bltabs"><ul class="clearfix"></ul></div><div class="pbl-tab-container" id="pbl-tabid"></div></div></div><div class="sidebar-col"><div class="lead-col js-lead-shadow" data-sidebar-fixed-container=""><div class="lead-wrapper"><div class="posrel"><div class="lead-module" data-lazymodule="lead" id="main_leaed_form"><script type="text/x-config">{"companyId":"100107487","companyName":"Veda """


soup = BeautifulSoup(main_text, 'html.parser')


# title = soup.title.text
# type = soup.find('span',{'class':'type'}).text
# carpet_area = soup.find('span',{'class':'size'}).text
# price = soup.find('meta', itemprop='price').get('content')
# status = soup.find('td',{'class':'val'}).text
# no_bathroom = soup.find('td',id="Bathrooms").get('title')
# description = soup.find('div', {'class': 'clearfix hidden'}).text.strip()
# facing = soup.find('td', {'id': 'Facing'}).text.strip()


# ==============================================================================================================
# ame = amenities = [i.text for i in soup.find_all('div',{'itemprop': 'amenityFeature'})]
ame_lst = []
# no_avail = []
for i in range(len(soup.find_all('div',{'class': 'outside-container'}))):
    main_html = soup.find_all('div',{'class': 'outside-container'})
    internal_ele = BeautifulSoup(str(main_html[i]), 'html.parser')
    

    try:
        if not re.search('<div class="overlay"></div>', str(internal_ele)):
            amenity = internal_ele.find('div',{'itemprop': 'amenityFeature'}).text

    except:
        amenity = None
    # na = soup.find('div',{'class':'overlay'}).text

    ame_lst.append(amenity)
    # no_avail.append(na)
    # print(f"{amenities} - {na}")
# print(ame_lst)
# <div class="overlay"></div>

# ====================================================================================================================
# print(no_avail)

# for i in soup.find_all('div',{'class': 'outside-container'}):
#     print(i, end="\n\n\n\n\n")


reg_text = "Thane East8.1Locality ScoreThane is also known as the City of Lake, famous for Masunda Lake, also known as Talao Pali . Thane is well connected to other regions by an extensive network of Railways and Roadways - including one...Know more about the Thane East"

ex = re.findall(r"\d{1}\.\d{1}", reg_text)
area = re.findall(r"(\w+\s?\w+)\d{1}",reg_text)
print(ex)



def getRandomProxy():
    proxy = {
    "http": f"http://scraperapi:e8ea2f46c786c0692dc03f363126ee27@proxy-server.scraperapi.com:8001",
    "https": f"http://scraperapi:e8ea2f46c786c0692dc03f363126ee27@proxy-server.scraperapi.com:8001"}

    return proxy

def getContent():
    # URL = input('Enter 99acres Property URL: ')
    urls = []
    for i in range(1):

        URL = "https://www.makaan.com/mumbai/builder-project-in-dadar-west-16253173/2bhk-2t-750-sqft-apartment"
        page = requests.get(URL, proxies=getRandomProxy(), verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')

        status = soup.find_all('td', id = "Status")[0].text.strip()

        print(status)

# getContent()

