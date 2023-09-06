from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.wikipediaspider import WikipediaspiderSpider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(WikipediaspiderSpider)
process.start()