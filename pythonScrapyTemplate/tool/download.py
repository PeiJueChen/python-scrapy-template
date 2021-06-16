import random
import socket
from time import sleep
from urllib.request import urlretrieve
import os
from multiprocessing import Queue
import threading

import requests

from pythonScrapyTemplate.tool.file import fileTool
from urllib.parse import quote
import string
FLAG = 'queue_flag_const'

# fileTool = File()


class Crawl_thread(threading.Thread):
    def __init__(self, thread_name, images_queue, carInfo, image_queue_flag, download_image_method) -> None:
        super(Crawl_thread, self).__init__()
        self.thread_name = thread_name
        self.images_queue = images_queue
        self.carInfo = carInfo
        self.image_queue_flag = image_queue_flag
        self.download_image_method = download_image_method

    def run(self) -> None:
        # return super().run()
        print('当前启动的处理任务为%s' % self.thread_name)
        while self.image_queue_flag[FLAG] == False:
            try:
                # 通过get方法，将里面的imageurlget出来,get为空的时候，抛异常
                url = self.images_queue.get(block=False)
                # name = self.carInfo['author']
                self.download_image_method(self.carInfo, url)
                # 可能停1秒
                sleep(random.randint(0, 1))
            except:
                print("except...")
                pass


class DownloadTask(object):
    def __init__(self) -> None:
        super().__init__()
        self.image_queue_flag = {FLAG: False}

    @property
    def agent(self):
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1  (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11     (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6  (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML,     like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1  (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML,  like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML,     like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3  (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML,     like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/    536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML,     like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3  (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML,     like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3  (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML,     like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML,     like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML,     like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24     (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        # 随机取一个值
        agent = random.choice(user_agent_list)
        return agent

    def addAgent(self, agent):
        import urllib.request
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',agent)]
        urllib.request.install_opener(opener)

    def reporthook(self, a, b, c):
        """
        显示下载进度
        :param a: 已经下载的数据块
        :param b: 数据块的大小
        :param c: 远程文件大小
        :return: None
        """
        try:
            print("\rdownloading: %5.1f%%" % (a * b * 100.0 / c), end="")
        except:
            pass

    def downloadImage(self, item, url):
        if not url or not item:
            print('missing url or carId')
            return
        author = item['author']
        fileName = item['name'] + '.rar'
        bookPath = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'books')
        carImagesPath = os.path.join(bookPath, author)
        fileTool.create_dir(carImagesPath)
        imagePath = os.path.join(carImagesPath, fileName)
        if fileTool.isExist(imagePath):
            print('fileName:%s is exist' % (fileName))
            return

        print('begin download:%s' % (fileName))
        try:

            # 因担心url 中有中文
            url = quote(url, safe=string.printable)

            # set timeout
            # socket.setdefaulttimeout(300)
            # self.addAgent(self.agent)
            # urlretrieve(url=url, filename=imagePath, reporthook=self.reporthook)


            # 300s
            r = requests.get(url, stream=True,timeout=300)
            f = open(imagePath, "wb")
            # chunk是指定每次写入的大小，每次只写了200byte
            try:
                for chunk in r.iter_content(chunk_size=200):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            except Exception as e1:
                print("Exception1:",e1)
            finally:
                f.close()
                r.close()

        except Exception as e:
            print(' download error:', e)
            pass

    def downloadItems(self, itemInfo):
        # print("JJ ~ file: download.py ~ line 47 ~ itemInfo", itemInfo)
        if not itemInfo:
            return
        urls = itemInfo['rarUrls']
        if not urls or len(urls) == 0:
            print('images the len is 0')
            return

        self.setupQueue(urls, itemInfo)

    def setupQueue(self, images, carInfo):
        # 开启队列
        images_queue = Queue()

        for image in images:
            images_queue.put(image)
        # for i in range(1, len(images)):
        #     images_queue.put(i)

        crawl_images_list = ["Image处理线程1号", "Image处理线程2号", "Image处理线程3号"]

        imagsLength = len(images)
        if imagsLength < 3:
            crawl_images_list.clear()
            for i in range(imagsLength):
                str = "Image处理线程{0}号".format(i+1)
                crawl_images_list.append(str)

        images_thread_list = []
        for images_thread in crawl_images_list:
            thread_ = Crawl_thread(
                images_thread, images_queue, carInfo, self.image_queue_flag, self.downloadImage)
            # 启动线程
            thread_.start()
            images_thread_list.append(thread_)

        while not images_queue.empty():
            pass
        self.image_queue_flag[FLAG] = True

        # 结束页码处理线程
        for thread_join in images_thread_list:
            thread_join.join()
            print(thread_join.thread_name, ': 处理结束')


# 这样相当是单例
# print('1')
# DownloadTask().downloadImage('h-354336','https://api.pjue.top/uploads/mdImages/1601994125093.png')
# print('2')
# DownloadTask().downloadImage('h-354336','https://www.imooc.com/static/img/index/logo.png')
# print('3')
# DownloadTask().downloadImage('h-354336','https://image1.guazistatic.com/qn210530190703e739b2d1d3690ff641b64efea7305ff0.jpg')
# print('4')
# DownloadTask().downloadImage('h-354335','https://api.pjue.top/uploads/mdImages/1601994125093.png')
# print('5')
# DownloadTask().downloadImage('h-354335','https://www.imooc.com/static/img/index/logo.png')
# print('6')
# DownloadTask().downloadImage('h-354335','https://image1.guazistatic.com/qn210530190703e739b2d1d3690ff641b64efea7305ff0.jpg')
# print('7')
