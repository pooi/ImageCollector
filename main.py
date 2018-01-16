from GoogleCollector import GoogleCollector
from BaiduCollector import BaiduCollector
from NaverCollector import NaverCollector
from BingCollector import BingCollector


keyword = input("Please input keyword : ")
try:
    max_image = int(input("Maximum number of download images(0:infinity) : "))
except:
    max_image = 0
try:
    threads = int(input("Number of threads(default is 8) : "))
except:
    threads = 8

collector = BaiduCollector(num_of_thread=threads)
collector.collectImage(keyword, max_image)

collector = BingCollector(num_of_thread=threads)
collector.collectImage(keyword, max_image)

collector = NaverCollector(num_of_thread=threads)
collector.collectImage(keyword, max_image)

collector = GoogleCollector(num_of_thread=threads)
collector.collectImage(keyword, max_image)