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
import os, sys, platform
import shutil
import eventlet
eventlet.monkey_patch()
from Downloader import Downloader
from queue import Queue

class BingCollector:

    def __init__(self, num_of_thread=8):
        if num_of_thread < 0:
            num_of_thread = 1

        self.error_list = []
        self.collectorName = "Bing_"
        self.num_of_thread = num_of_thread
        self.pre_img_count = 0

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

    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=30, fill='#'):
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

    def checkImageCount(self, source, maximum=0):
        soup = bs(str(source), "html.parser")
        links = soup.find_all("li", class_="imgitem")
        num_of_image = len(links)

        if self.pre_img_count == num_of_image:
            return True

        if maximum <= 0:
            return False

        return num_of_image > maximum

    def search(self, keyword, maximum=0):
        self.print_with_color("Search Result...", "b")

        url = "https://www.bing.com/images/search?q=" + keyword + "&qs=n&form=QBLH&scope=images&sp=-1&pq=" + keyword

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
                isFinish = self.checkImageCount(browser.page_source, maximum=maximum)
                if isFinish:
                    self.printProgressBar(num_of_scroll * num_of_down, num_of_scroll * num_of_down, prefix='Scroll Down:', suffix='Complete')
                    break
            if isFinish:
                break
            time.sleep(0.2)

        # Get page source and close the browser
        source = browser.page_source
        browser.close()


        # Get image urls
        soup = bs(str(source), "html.parser")
        links = soup.find_all("img", class_="mimg")
        self.print_with_color("Find %d images" % len(links), "g")

        return links

    def collect_image_URL(self, links, max):
        self.print_with_color("Collect Image URL...", "b")

        collect = []

        num_of_links = len(links)
        self.printProgressBar(0, num_of_links, prefix='Progress:', suffix='Complete')
        for i in range(num_of_links):
            self.printProgressBar(i+1, num_of_links, prefix='Progress:', suffix='Complete')
            link = links[i]

            img = ""
            try:
                img1 = link['src']
                img1 = str(img1)
                if not img1.startswith("http"):
                    img1 = "http://" + img1

                if img is "":
                    img = img1
                else:
                    img = img + "#" + img1
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

        thread_count = self.num_of_thread

        queue = Queue()

        self.printProgressBar(0, len(collects), prefix='Progress:', suffix='Complete')
        for i in range(thread_count):
            downloader = Downloader(queue, dir, self.collectorName, self.error_list, len(collects))
            downloader.daemon = True
            downloader.start()

        for i in range(len(collects)):
            url = collects[i]
            queue.put(url)

        queue.join()

        self.printProgressBar(len(collects), len(collects), prefix='Progress:', suffix='Complete')

        # Start download
        # self.printProgressBar(0, len(collects), prefix='Progress:', suffix='Complete')
        # for i in range(len(collects)):
        #     self.printProgressBar(i+1, len(collects), prefix='Progress:', suffix='Complete')
        #     # print("Download Image (%d/%d)" % (i+1, len(collects)))
        #     col = collects[i]
        #     if (col == '알림'):
        #         pass
        #     else:
        #         full_name = self.collectorName + str(i+1) + ".jpg"
        #         save_path = os.path.join(dir, full_name)  # 저장폴더
        #
        #         try:
        #             with eventlet.Timeout(self.DOWNLOAD_TIMEOUT):
        #                 urllib2.urlretrieve(col, save_path)
        #         except:
        #             self.error_list.append(col)

        self.print_with_color("Save %d images" % (len(collects) - len(self.error_list)), "g")

    def collectImage(self, keyword, max=0):

        print()
        self.print_with_color("Collect %s images from Bing" % keyword, "r")

        links = self.search(keyword, max)

        collect = self.collect_image_URL(links, max)

        self.download(collect, keyword)

        # if len(self.error_list) > 0:
        #     print("Error list")
        #     for err in self.error_list:
        #         print(err)
