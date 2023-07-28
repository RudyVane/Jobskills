from os import environ
import tldextract
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import scraper.spiders as spiders
from scrapy.utils.project import get_project_settings
from crochet import setup
setup()
settings = get_project_settings()
configure_logging(settings) 

readability_blacklist = ["indeed"]

def getSpider(url):
    ret = spiders.ReadabilitySpider
    tld = tldextract.extract(url)
    if(tld.domain in readability_blacklist):
        ret = spiders.GenericSpider
    match(tld.domain):
        case "indeed":
            ret = spiders.IndeedSpider
    
    print(ret)
    return ret

def transformUrl(url):
    return "https://webcache.googleusercontent.com/search?q=cache:"+url

def scrape(url, cb):
    res = []
    print(settings)
    class ResPipeline(object):
        def process_item(self, item, spider):
            res.append(dict(item))
            return item
    
    settings.set("ITEM_PIPELINES", {**settings.get("ITEM_PIPELINES"), ResPipeline: 1000})
    runner = CrawlerRunner(settings)
    s = getSpider(url)
    d = runner.crawl(s, start_urls=[transformUrl(url)], )
    d.addCallback(lambda _: cb(res))
