import logging

import tldextract
from arq.connections import RedisSettings
from crochet import setup
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.defer import deferred_to_future
from scrapy.utils.log import configure_logging

from jobskills.config import settings
from jobskills.scraper.spiders.generic import Spider as genSpider
from jobskills.scraper.spiders.indeed import Spider as indSpider
from jobskills.scraper.spiders.readability import Spider as readSpider

# spiders = {
#     k: importlib.import_module(k, "jobskills.scraper.spiders").Spider
#     for k in ["generic", "readability", "indeed"]
# }

spiders = {"generic": genSpider, "readability": readSpider, "indeed": indSpider}


setup()
logger = logging.getLogger(__name__)

scrapy_settings = Settings(
    {
        k: getattr(settings.scraper.scrapy, k)
        for k in dir(settings.scraper.scrapy)
        if not k.startswith("_")
    }
)
configure_logging(scrapy_settings)


async def startup(ctx):
    ctx["blacklists"] = settings.scraper.blacklists
    ctx["domains"] = settings.scraper.domains
    logger.info("Initialized scraper worker")


async def shutdown(ctx):
    pass


async def getSpider(ctx, url):
    tld = tldextract.extract(url)
    print(tld)
    smod_name = (
        ctx["domains"].get(tld.domain) or ctx["domains"].get("_default") or {}
    ).get("spider", "generic")
    smod = spiders.get(smod_name)
    print(smod)
    return smod


async def transformUrl(ctx, url):
    tld = tldextract.extract(url)
    return (
        (ctx["domains"].get(tld.domain) or ctx["domains"].get("_default"))
        .get("transform", "{}")
        .format(url)
    )


def _nop(_):
    pass


# @wait_for(timeout=10)
async def _scrape(ctx, url, cb=_nop):
    res = {}
    print(scrapy_settings)

    class ResPipeline(object):
        def process_item(self, item, spider):
            res.update(dict(item))
            return item

    scrapy_settings.set(
        "ITEM_PIPELINES", {**scrapy_settings.get("ITEM_PIPELINES"), ResPipeline: 1000}
    )
    runner = CrawlerRunner(scrapy_settings)
    s = await getSpider(ctx, url)
    print(s)
    d = runner.crawl(
        s,
        start_urls=[await transformUrl(ctx, url)],
    )
    d.addCallback(lambda _: cb(res))
    await deferred_to_future(d)
    return res


async def scrape(ctx, url, cb=_nop):
    return await _scrape(ctx, url, cb=cb)


class WorkerSettings:
    functions = [scrape]
    queue_name = "arq:scraper"
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(settings.redis.dsn)
