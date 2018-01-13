# -*- coding:utf-8 -*-
import requests
import time

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import os, sys, platform
import shutil
import eventlet
eventlet.monkey_patch()

class BaiduCollector:

    def __init__(self):
        self.ua = UserAgent()
        # self.collect = []
        self.error_list = []
        self.collectorName = "Baidu_"

        self.TEXT_BLUE = '\033[94m'
        self.TEXT_ENDC = '\033[0m'
        self.TEXT_GREEN = '\033[92m'
        self.TEXT_RED = '\033[93m'

        self.PROGRESS_LEN = 30
        self.DOWNLOAD_TIMEOUT = 20

    def print_with_color(self, text, color="none"):

        if platform.platform().lower().startswith("win"):
            print(text)
            return

        if color is "b":
            print(self.TEXT_BLUE + text + self.TEXT_ENDC)
        elif color is "g":
            print(self.TEXT_GREEN + text + self.TEXT_ENDC)
        elif color is "r":
            print(self.TEXT_RED + text + self.TEXT_ENDC)
        else:
            print(text)

    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=30, fill='█'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
        # Print New Line on Complete
        if iteration == total:
            print()


    def search(self, keyword):
        self.print_with_color("Search Result...", "b")

        url = "http://image.baidu.com/search/index?tn=baiduimage&fm=result&ie=utf-8&word=" + keyword

        # Create a browser
        if platform.platform().lower().startswith("win"):
            dir = os.getcwd() + '/chromedriver_win'
        elif platform.platform().lower().startswith("darwin"):
            dir = os.getcwd() + '/chromedriver_mac'
        elif platform.platform().lower().startswith("linux"):
            dir = os.getcwd() + '/chromedriver_linux'
        else:
            dir = os.getcwd() + '/chromedriver_mac'

        browser = webdriver.Chrome(dir)

        # Open the link
        browser.get(url)

        element = browser.find_element_by_tag_name("body")

        # Scroll down
        num_of_scroll = 10 # 10
        num_of_down = 100 # 100
        count = 0
        self.printProgressBar(0, num_of_scroll*num_of_down, prefix='Scroll Down:', suffix='Complete')
        for i in range(1, num_of_scroll+1):
            for j in range(1, num_of_down+1):
                element.send_keys(Keys.PAGE_DOWN)
                count += 1
                self.printProgressBar(count, num_of_scroll * num_of_down, prefix='Scroll Down:', suffix='Complete')
            # print("Scroll Down (%d/%d)" % (i+1, num_of_scroll))
            time.sleep(0.2)

        # Get page source and close the browser
        source = browser.page_source
        browser.close()


        # Get image urls
        soup = bs(str(source), "html.parser")
        links = soup.find_all("li", class_="imgitem")
        self.print_with_color("Find %d images" % len(links), "g")

        return links

    def collect_image_URL(self, links, max):
        self.print_with_color("Collect Image URL...", "b")

        collect = []
        headers = {"User-Agent": self.ua.random}

        num_of_links = len(links)
        self.printProgressBar(0, num_of_links, prefix='Progress:', suffix='Complete')
        for i in range(num_of_links):
            self.printProgressBar(i+1, num_of_links, prefix='Progress:', suffix='Complete')
            link = links[i]

            img = ""
            try:
                img1 = link['data-thumburl']
                img1 = str(img1)
                if not img1.startswith("http"):
                    img1 = "http://" + img1

                if img is "":
                    img = img1
                else:
                    img = img + "#" + img1
            except:
                pass

            try:
                img2 = link.find('img')['data-imgurl']
                if not img2.startswith("http"):
                    img2 = "http://" + img2

                if img is "":
                    img = img2
                else:
                    img = img + "#" + img2
            except:
                pass

            try:
                img3 = link['data-objurl']
                if not img3.startswith("http"):
                    img3 = "http://" + img3

                if img is "":
                    img = img3
                else:
                    img = img + "#" + img3
            except:
                pass

            collect.append(img)

            if max > 0:
                if i > max:
                    self.printProgressBar(num_of_links, num_of_links, prefix='Progress:', suffix='Complete')
                    break

        return collect

    def download(self, collects, keyword):
        self.print_with_color("Download Images...", "b")

        image_count = 0

        keyword = 'images/' + keyword

        # Make directory and path
        if not os.path.isdir(keyword):
            print("Make a directory.")
            os.makedirs(keyword)

        dir = os.getcwd() + "/" + str(keyword)
        # os.chdir(dir)
        self.print_with_color("Download path is %s" % dir, "g")

        if not dir.endswith("/"):
            dir += '/'

        # Start download
        self.printProgressBar(0, len(collects), prefix='Progress:', suffix='Complete')
        for i in range(len(collects)):
            self.printProgressBar(i+1, len(collects), prefix='Progress:', suffix='Complete')
            # print("Download Image (%d/%d)" % (i+1, len(collects)))
            col = collects[i]
            if (col == '알림'):
                pass
            else:
                full_name = self.collectorName + str(i+1) + ".jpg"
                save_path = os.path.join(dir, full_name)  # 저장폴더

                try:
                    urllib2.urlretrieve(col, save_path)
                except:
                    self.error_list.append(col)

                isFail = True
                for img in col.split("#"):
                    try:
                        with eventlet.Timeout(self.DOWNLOAD_TIMEOUT):
                            urllib2.urlretrieve(img, save_path)
                        # with eventlet.Timeout(self.DOWNLOAD_TIMEOUT):
                        #     r = requests.get(img, stream=True, headers={'User-agent': 'Mozilla/5.0'})
                        # if r.status_code == 200:
                        #     with open(save_path, 'wb') as f:
                        #         r.raw.decode_content = True
                        #         with eventlet.Timeout(self.DOWNLOAD_TIMEOUT):
                        #             shutil.copyfileobj(r.raw, f)
                        isFail = False
                        break
                        # else:
                        #     isFail = True
                    except:
                        isFail = True

                if isFail:
                    self.error_list.append(col)

        self.print_with_color("Save %d images" % (len(collects) - len(self.error_list)), "g")

    def collectImage(self, keyword, max=0):

        self.print_with_color("Collect %s images from Baidu" % keyword, "r")

        links = self.search(keyword)

        collect = self.collect_image_URL(links, max)

        self.download(collect, keyword)

        # if len(self.error_list) > 0:
        #     print("Error list")
        #     for err in self.error_list:
        #         print(err)




