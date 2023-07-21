from os import environ
from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
import scraper.spiders as spiders
from scrapy.utils.project import get_project_settings
from crochet import setup
setup()

def getSpider(url):
    return spiders.IndeedSpider

def transformUrl(url):
    return "https://webcache.googleusercontent.com/search?q=cache:"+url

def scrape(url, cb):
    res = []
    settings = get_project_settings()
    class ResPipeline(object):
        def process_item(self, item, spider):
            res.append(dict(item))
            return item
    runner = CrawlerRunner(settings)
    settings.set("ITEM_PIPELINES", {**settings.get("ITEM_PIPELINES"), ResPipeline: 1000})
    d = runner.crawl(getSpider(url), start_urls=[transformUrl(url)])
    d.addCallback(lambda _: cb(res))
