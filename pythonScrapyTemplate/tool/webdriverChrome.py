from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
import random

# https://www.cnblogs.com/jxldjsn/p/7399263.html


class WebdriverChrome(object):

    __myB = None

    def __init__(self) -> None:
        super().__init__()

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

    def getOptions(self, referer=""):
        chrome_options = webdriver.ChromeOptions()
        # 使用headless无界面浏览器模式，即不需要打开浏览器
        chrome_options.add_argument('--headless')  # 增加无界面选项
        chrome_options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(
            'user-agent="{0}"'.format(self.agent))
        if referer and len(referer) > 0:
            chrome_options.add_argument('Referer="{0}"'.format(referer))

        return chrome_options

    @property
    def getMyDriver(self):
        return self.__myB

    def get(self, url, referer=""):
        # 建立Chrome的驱动
        self.__myB = webdriver.Chrome(options=self.getOptions(referer))
        # 最大窗口
        self.__myB.maximize_window()
        # 隐式等待，动态查找元素
        self.__myB.implicitly_wait(10)

        self.__myB.get(url)

        return self.__myB

        # get element by xpath
        # a = b.find_element_by_xpath(
        #     "//div[@class='area']//div[@class='gohome l']//h1/a")
        # name = a.get_attribute('innerHTML')
        # # href = a.get_attribute('href')

        # # 进入iframe内嵌网页
        # # b.switch_to.frame("playbox")
        # b.switch_to.frame(b.find_elements_by_tag_name("iframe")[0])

        # video = b.find_element_by_class_name('video')
        # url = self.getAttribute(video,'url')

        # html = b.page_source  # 打印页面
        # soup = BeautifulSoup(html, "html.parser")
        # # 以标准格式输出
        # prettify = soup.prettify()

        # html = etree.HTML(prettify)
        # url = html.xpath("//*[@id='dplayer']//video/@src")[0]

    def find_element_by_xpath(self, xpath):
        if not self.__myB:
            print('Please run get method')
            return
        return self.__myB.find_element_by_xpath(xpath)

    def switch_to_default(self):
        if not self.__myB:
            print('Please run get method')
            return
        self.__myB.switch_to.default_content()

    def switch_to_frame(self, element):
        if not self.__myB:
            print('Please run get method')
            return
        self.__myB.switch_to.frame(element)

    # innerHTML / href
    def getAttribute(self, element, attribute):
        return element.get_attribute(attribute)

    # can use xpath, 传入的html 最好经过美化
    def etreeHtml(self, html):
        # 打印解析内容str
        # t = etree.tostring(etree.HTML(html), encoding="utf-8", pretty_print=True)
        return etree.HTML(html)

    # 美化, 建议使用etree
    def prettify(self):
        if not self.__myB:
            print('Please run get method')
            return
        html = self.HTML_PAGE(self.__myB)
        return BeautifulSoup(html, "html.parser").prettify()

    # page
    def HTML_PAGE(self):
        if not self.__myB:
            print('Please run get method')
            return
        return self.__myB.page_source


myWebdriver = WebdriverChrome()
