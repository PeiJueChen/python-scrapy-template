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
from contextlib import closing


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


class ProgressBar(object):

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


FLAG = 'queue_flag_const'


class Crawl_thread(threading.Thread):
    def __init__(self, thread_name, queues_, queue_flag, download_method) -> None:
        super(Crawl_thread, self).__init__()
        self.thread_name = thread_name
        self.queues_ = queues_
        self.queue_flag = queue_flag
        self.download_method = download_method

    def run(self) -> None:
        # return super().run()
        print('当前启动的处理任务为%s' % self.thread_name)
        while self.queue_flag[FLAG] == False:
            try:
                # 通过get方法，将里面的imageurlget出来,get为空的时候，抛异常
                urlObject = self.queues_.get(block=False)
                self.download_method(urlObject)
                # 可能停1秒
                sleep(random.randint(0, 1))
            except Exception as e:
                print("except...", e)
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

    def downloadFile(self, urlObject):
        """
            urlObject: {
                url: xxx, (required)
                folderName:xxx, (optional)
                fileName:xxx (required)
            }
        """
        if not urlObject:
            print('missing urlObject')
            return

        urlObject = dict(urlObject)
        folderName = urlObject.get("folderName", "")

        url = urlObject.get('url', None)
        fileName = urlObject.get("fileName", None)

        if not url or not fileName:
            print("missing url or filename")
            return

        path_ = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'download-files')
        itemPath = path_

        if folderName and len(folderName) > 0:
            itemPath = os.path.join(path_, folderName)

        fileTool.create_dir(itemPath)

        itemFullPath = os.path.join(itemPath, fileName)
        if fileTool.isExist(itemFullPath):
            print('fileName:%s is exist' % (fileName))
            return

        try:
            print('%s >>> Start Downloading...' % (fileName))
            # 因担心url 中有中文
            url = quote(url, safe=string.printable)

            # set timeout
            # socket.setdefaulttimeout(300)
            # self.addAgent(self.agent)
            # urlretrieve(url=url, filename=itemFullPath, reporthook=self.reporthook)

            # 单次请求最大值
            chunk_size = 1024
            # 300s
            timeout = 300
            with closing(requests.get(url, stream=True, timeout=timeout)) as response:
                # 内容体总大小
                content_size = int(response.headers['content-length'])
                progress = ProgressBar(fileName, total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
                with open(itemFullPath, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        file.flush()
                        progress.refresh(count=len(data))

            print('%s >>> End Downloading...' % (fileName))

        except Exception as e:
            print('download error:', e)
            pass

    def downloadItems(self, urlObjects):
        """
            urlObjects : [{
                url: xxx, (required)
                folderName:xxx, (optional)
                fileName:xxx (required)
            }]
        """
        if not urlObjects:
            print('missing urlObjects')
            return
        # urls = itemInfo[urlKey]
        if len(urlObjects) == 0:
            print('urlObjects the len is 0')
            return

        self.setupQueue(urlObjects)

    def setupQueue(self, urlObjects):
        # 开启队列
        task_queues = Queue()

        for url in urlObjects:
            task_queues.put(url)

        crawl_urls_list = ["Task处理线程1号", "Task处理线程2号", "Task处理线程3号"]

        urlsLength = len(urlObjects)
        if urlsLength < 3:
            crawl_urls_list.clear()
            for i in range(urlsLength):
                str = "Task处理线程{0}号".format(i+1)
                crawl_urls_list.append(str)

        url_thread_list = []
        for url_thread in crawl_urls_list:
            thread_ = Crawl_thread(
                url_thread, task_queues, self.queue_flag, self.downloadFile)
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
# urls = [{
#     "url": 'https://api.pjue.top/uploads/mdImages/1601994125093.png',
#     'fileName': '1601994125092.png',
#     "folderName": 'pnpn'
# }]
# DownloadTask().downloadItems(urls)
