# DownloadTask class
import random
import socket
from time import sleep
from urllib.request import urlretrieve
import os
from multiprocessing import Queue
import threading
import requests
from urllib.parse import quote
import string

class File(object):
    def writeFile(self, content, name="1.html"):
        path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'file-contents')
        self.create_dir(path)
        fullPath = os.path.join(path, name)
        f = None
        try:
            f = open(fullPath, 'w', encoding="utf-8")
            f.write(content)
            f.flush()
        finally:
            if f:
                f.close()

    def create_dir(self, dir_path):
        # if not os.path.exists(dir_path): os.mkdir(dir_path)
        # 可以创建多层
        if not self.isExist(dir_path):
            os.makedirs(dir_path)

    def isExist(self, dir_path):
        return os.path.exists(dir_path)

    def getCurrentFilePath():
        return os.path.dirname(os.path.dirname(__file__))

fileTool = File()


FLAG = 'queue_flag_const'

class Crawl_thread(threading.Thread):
    def __init__(self, thread_name, queues_, itemInfo, queue_flag, download_method) -> None:
        super(Crawl_thread, self).__init__()
        self.thread_name = thread_name
        self.queues_ = queues_
        self.itemInfo = itemInfo
        self.queue_flag = queue_flag
        self.download_method = download_method

    def run(self) -> None:
        # return super().run()
        print('当前启动的处理任务为%s' % self.thread_name)
        while self.queue_flag[FLAG] == False:
            try:
                # 通过get方法，将里面的imageurlget出来,get为空的时候，抛异常
                url = self.queues_.get(block=False)
                # name = self.carInfo['author']
                self.download_method(self.itemInfo, url)
                # 可能停1秒
                sleep(random.randint(0, 1))
            except:
                print("except...")
                pass


class DownloadTask(object):
    def __init__(self) -> None:
        super().__init__()
        self.queue_flag = {FLAG: False}

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
        opener.addheaders = [('User-Agent', agent)]
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
            print("\rdownloading: %5.1f%%" % (a * b * 100.0 / c), end="done")
        except:
            pass

    def downloadFile(self, item, url):
        if not url or not item:
            print('missing url or carId')
            return

        # set多层路径 xxx/author/name
        author = item['author']
        # fileName = item['name'] + '.png'
        # 请自行添加后缀
        fileName = item['name']

        path_ = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'download-files')
        itemPath = os.path.join(path_, author)
        fileTool.create_dir(itemPath)
        itemFullPath = os.path.join(itemPath, fileName)
        if fileTool.isExist(itemFullPath):
            print('fileName:%s is exist' % (fileName))
            return

        print('begin download:%s' % (fileName))
        try:

            # 因担心url 中有中文
            url = quote(url, safe=string.printable)

            # set timeout
            # socket.setdefaulttimeout(300)
            # self.addAgent(self.agent)
            # urlretrieve(url=url, filename=itemFullPath, reporthook=self.reporthook)

            # 300s
            r = requests.get(url, stream=True, timeout=300)
            f = open(itemFullPath, "wb")
            # chunk是指定每次写入的大小，每次只写了200byte
            try:
                for chunk in r.iter_content(chunk_size=200):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            except Exception as e1:
                print("write error:", e1)
            finally:
                f.close()
                r.close()
                print('end download:%s' % (fileName))

        except Exception as e:
            print('download error:', e)
            pass

    def downloadItems(self, itemInfo, urlKey):
        if not itemInfo or not urlKey:
            return
        urls = itemInfo[urlKey]
        if not urls or len(urls) == 0:
            print('urls the len is 0')
            return

        self.setupQueue(urls, itemInfo)

    def setupQueue(self, urls, itemInfo):
        # 开启队列
        task_queues = Queue()

        for url in urls:
            task_queues.put(url)
        crawl_urls_list = ["Task处理线程1号", "Task处理线程2号", "Task处理线程3号"]

        urlsLength = len(urls)
        if urlsLength < 3:
            crawl_urls_list.clear()
            for i in range(urlsLength):
                str = "Task处理线程{0}号".format(i+1)
                crawl_urls_list.append(str)

        url_thread_list = []
        for url_thread in crawl_urls_list:
            thread_ = Crawl_thread(
                url_thread, task_queues, itemInfo, self.queue_flag, self.downloadFile)
            # 启动线程
            thread_.start()
            url_thread_list.append(thread_)

        while not task_queues.empty():
            pass

        self.queue_flag[FLAG] = True

        # 结束页码处理线程
        for thread_join in url_thread_list:
            thread_join.join()
            print(thread_join.thread_name, ': 处理结束')

# USE
# item = {"author": 'author1', 'name': 'filename.png'}
# urls = '表示item 中哪个属性保存着urls: 比如: fileUrls'
# DownloadTask().downloadItems(item, urls)


# DownloadTask().downloadFile({'author': 'test', 'name': 'test3'},'https://api.pjue.top/uploads/mdImages/1601994125093.png')

