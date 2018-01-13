from GoogleCollector import GoogleCollector
from BaiduCollector import BaiduCollector
from NaverCollector import NaverCollector
from BingCollector import BingCollector


keyword = input("Please input keyword : ")
max_image = int(input("Maximum number of download images(0:infinity) : "))

collector = BaiduCollector()
collector.collectImage(keyword, max_image)

collector = BingCollector()
collector.collectImage(keyword, max_image)

collector = NaverCollector()
collector.collectImage(keyword, max_image)

collector = GoogleCollector()
collector.collectImage(keyword, max_image)