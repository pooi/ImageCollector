import argparse

from GoogleCollector import GoogleCollector
from BaiduCollector import BaiduCollector
from NaverCollector import NaverCollector
from BingCollector import BingCollector

parser = argparse.ArgumentParser()
parser.add_argument("--baidu", help="If this value is 0, baidu will not be used to collect images.")
parser.add_argument("--bing", help="If this value is 0, bing will not be used to collect images.")
parser.add_argument("--naver", help="If this value is 0, naver will not be used to collect images.")
parser.add_argument("--google", help="If this value is 0, google will not be used to collect images.")
args = parser.parse_args()

isBaidu = True
isBing = True
isNaver = True
isGoogle = True

if args.baidu:
    try:
        c = int(args.baidu)
        isBaidu = (c != 0)
    except:
        pass
if args.bing:
    try:
        c = int(args.bing)
        isBing = (c != 0)
    except:
        pass
if args.naver:
    try:
        c = int(args.naver)
        isNaver = (c != 0)
    except:
        pass
if args.google:
    try:
        c = int(args.google)
        isGoogle = (c != 0)
    except:
        pass

keywords = input("Please input keyword(Multiple keywords can be entered using commas.) : ")
keywords.encode('utf-8')
try:
    max_image = int(input("Maximum number of download images(0:infinity) : "))
except:
    max_image = 0
try:
    threads = int(input("Number of threads(default is 8) : "))
except:
    threads = 8

for keyword in keywords.split(","):

    print("Collect", keyword)

    if isBaidu:
        collector = BaiduCollector(num_of_thread=threads)
        collector.collectImage(keyword, max_image)

    if isBing:
        collector = BingCollector(num_of_thread=threads)
        collector.collectImage(keyword, max_image)

    if isNaver:
        collector = NaverCollector(num_of_thread=threads)
        collector.collectImage(keyword, max_image)

    if isGoogle:
        collector = GoogleCollector(num_of_thread=threads)
        collector.collectImage(keyword, max_image)