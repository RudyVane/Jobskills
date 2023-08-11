import asyncio
# from twisted.internet import asyncioreactor, reactor
# from twisted.internet.defer import inlineCallbacks, returnValue
import sys
from os import environ
import tldextract
import json
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import spiders
import settings as s
from scrapy.settings import Settings
from crochet import setup
setup()
from scrapy.utils.defer import deferred_to_future

# if "twisted.internet.reactor" in sys.modules:
#     del sys.modules["twisted.internet.reactor"]
# asyncioreactor.install()

# settings = get_project_settings()
settings = Settings({k: getattr(s, k) for k in dir(s) if not k.startswith("_")})
configure_logging(settings)

blacklists = {}
domains = {}

async def startup(ctx):
    f = open("blacklists.json")
    ctx["blacklists"] = json.loads(f.read())
    f.close()

    f = open("domains.json")
    ctx["domains"] = json.loads(f.read())
    f.close()

async def shutdown(ctx):
    pass

async def getSpider(ctx, url):
    tld = tldextract.extract(url)
    if tld.domain in ctx["blacklists"]["readability"] and not tld.domain in dir(ctx["domains"]):
        return spiders.GenericSpider
    return getattr(spiders, (ctx["domains"].get(tld.domain) or ctx["domains"].get("__default__")).get("spider", "GenericSpider"))


async def transformUrl(ctx, url):
    tld = tldextract.extract(url)
    return (ctx["domains"].get(tld.domain) or ctx["domains"].get("__default__")).get("transform", "{}").format(url)

def _nop(_):
    pass

# @wait_for(timeout=10)
async def _scrape(ctx, url, cb = _nop):
    res = {}
    print(settings)

    class ResPipeline(object):
        def process_item(self, item, spider):
            res.update(dict(item))
            return item

    settings.set(
        "ITEM_PIPELINES", {**settings.get("ITEM_PIPELINES"), ResPipeline: 1000}
    )
    runner = CrawlerRunner(settings)
    s = await getSpider(ctx, url)
    print(s)
    d = runner.crawl(
        s,
        start_urls=[
            await transformUrl(ctx, url)
            ],
    )
    d.addCallback(lambda _: cb(res))
    await deferred_to_future(d)
    return res

async def scrape(ctx, url, cb = _nop):
    return await _scrape(ctx, url, cb = cb)

class WorkerSettings:
    functions = [scrape]
    on_startup = startup
    on_shutdown = shutdown