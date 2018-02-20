try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import eventlet
from urllib.request import urlopen, Request
import json
import os
from threading import Thread
from queue import Queue

import string
import random

class Downloader(Thread):

    def __init__(self, queue, folder, collectorName, error_list, total_count, is_multiple_url=False):
        Thread.__init__(self)
        self.queue = queue
        self.folder = folder
        self.collectorName = collectorName
        self.error_list = error_list
        self.total_count = total_count
        self.is_multiple_url = is_multiple_url

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
        try:
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)
            print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
            # Print New Line on Complete
            if iteration == total:
                print()
        except:
            pass

    def str_generator(self, size=10, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def download_images(self, target_dir, url, index):

        full_name = self.collectorName + str(index + 1) + ".jpg"
        save_path = os.path.join(target_dir, full_name)  # 저장폴더

        try:
            with eventlet.Timeout(20):
                urllib2.urlretrieve(url, save_path)
        except:
            self.error_list.append(url)
        finally:
            if not self.queue.qsize() == 0:
                self.printProgressBar(self.total_count - self.queue.qsize(), self.total_count, prefix='Progress:', suffix='Complete')
        # path = target_dir + '/' + os.path.basename(url)
        #
        # with open(path, 'wb') as file:
        #     file.write(urlopen(url).read())

    def download_images_with_multiple_url(self, target_dir, url, index):

        full_name = self.collectorName + str(index + 1) + "_" + self.str_generator() + ".jpg"
        save_path = os.path.join(target_dir, full_name)  # 저장폴더

        try:
            isFail = True
            for img in url.split("#"):
                try:
                    with eventlet.Timeout(20):
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
                self.error_list.append(url)
        except:
            self.error_list.append(url)
        finally:
            if not self.queue.qsize() == 0:
                self.printProgressBar(self.total_count - self.queue.qsize(), self.total_count, prefix='Progress:', suffix='Complete')

    def run(self):
        while True:
            url = self.queue.get()
            index = self.total_count - self.queue.qsize() -1
            if self.is_multiple_url:
                self.download_images_with_multiple_url(self.folder, url, index)
            else:
                self.download_images(self.folder, url, index)
            self.queue.task_done()