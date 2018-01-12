from GoogleCollector import GoogleCollector

collector = GoogleCollector()

keyword = input("Please input keyword : ")
max_image = int(input("Maximum number of download images(0:infinity) : "))

collector.collectImage(keyword, max_image)