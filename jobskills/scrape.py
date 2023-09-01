import json
from os import environ

import tldextract
from crochet import setup
from scraper import settings as s
from scraper import spiders
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

setup()
# settings = get_project_settings()
settings = Settings({k: getattr(s, k) for k in dir(s) if not k.startswith("_")})
configure_logging(settings)

f = open("scraper/blacklists.json")
blacklists = json.loads(f.read())
f.close()

f = open("scraper/domains.json")
domains = json.loads(f.read())
f.close()


def getSpider(url):
    tld = tldextract.extract(url)
    if tld.domain in blacklists["readability"] and not tld.domain in dir(domains):
        return spiders.GenericSpider
    return getattr(
        spiders,
        (domains.get(tld.domain) or domains.get("__default__")).get(
            "spider", "GenericSpider"
        ),
    )


def transformUrl(url):
    tld = tldextract.extract(url)
    return (
        (domains.get(tld.domain) or domains.get("__default__"))
        .get("transform", "{}")
        .format(url)
    )


def scrape(url, cb):
    res = []
    print(settings)

    class ResPipeline(object):
        def process_item(self, item, spider):
            res.append(dict(item))
            return item

    settings.set(
        "ITEM_PIPELINES", {**settings.get("ITEM_PIPELINES"), ResPipeline: 1000}
    )
    runner = CrawlerRunner(settings)
    s = getSpider(url)
    d = runner.crawl(
        s,
        start_urls=[transformUrl(url)],
    )
    d.addCallback(lambda _: cb(res))
