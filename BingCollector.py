# -*- coding:utf-8 -*-
import requests
import time

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import argparse
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from multiprocessing import Pool
from lxml.html import fromstring
import os, sys

class BingCollector:
    def __init__(self):
        self.ua = UserAgent()
        self.collect = []
        self.error_list = []

    def search(self, url):
        print("Search Result..")
        # Create a browser
        browser = webdriver.Chrome("C:\chromedriver_win32\chromedriver")
            
        # Open the link
        browser.get(url)
        time.sleep(1)

        element = browser.find_element_by_tag_name("body")

        # # Scroll down
        for i in range(15):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

        time.sleep(1)

        # Get page source and close the browser
        source = browser.page_source
        browser.close()
        return source
    
    def download(self, collects, dir='/'):
        print("Download Image..")
        if not dir.endswith("/"):
            dir += '/'


        for i in range(len(collects)):
            print("%d/%d"%(i, len(collects)))
            col = collects[i]
            if (col == '알림'):
                pass
            else:
                full_name = str(collects.index(col)) + ".jpg"
                save_path = os.path.join(dir, full_name)  # 저장폴더
                try:
                    urllib2.urlretrieve(col, save_path)
                except:
                    self.error_list.append(col)
                    pass

    def download_image(self, link):
        # Use a random user agent header
        headers = {"User-Agent": self.ua.random}
        print(link.get("src"))
        # Get the image link
        #try:
            #r = requests.get(link.get("src"), headers=headers)
        #except:
            #print("Cannot get link.")
        #title = str(fromstring(r.content).findtext(".//title"))
        #print(title)
        link = link.get("src")
        print(link)
        self.collect.append(link)
        # Downlo    ad the image

    def collectImage(self, keyword):
        url = "https://www.bing.com/images/search?q="+keyword+"&qs=n&form=QBLH&scope=images&sp=-1&pq="+keyword
        source = self.search(url)

        # Parse the page source and download pics
        soup = bs(str(source), "html.parser")
        links = soup.find_all("img", class_="mimg")
        print("%d개 이미지가 검색됨"%len(links))
        if not os.path.isdir(keyword):
            os.makedirs(keyword)

        dir = os.getcwd() + "/" + str(keyword)
        os.chdir(dir)
        print(dir)

        print("Collect Image URL..")
        for link in links:
            self.download_image(link)

        # print(collect)
        self.download(self.collect, dir)        
