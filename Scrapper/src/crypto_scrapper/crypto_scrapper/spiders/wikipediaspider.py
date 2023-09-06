import scrapy


class WikipediaspiderSpider(scrapy.Spider):
    name = "wikipediaspider"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org"]

    def parse(self, response):
        print(response)
        pass
