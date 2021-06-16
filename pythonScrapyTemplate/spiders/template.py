import scrapy


class TemplateSpider(scrapy.Spider):
    name = 'template'
    allowed_domains = ['xxxx.com']
    start_urls = ['https://www.baidu.com/']

    # def start_requests(self):
    #     pass

    def parse(self, response):
        print('response:',response.text)
        pass
