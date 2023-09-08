import json
import os
from operator import attrgetter

import tldextract
from crochet import setup
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.defer import deferred_to_future
from scrapy.utils.log import configure_logging

from jobskills.jobqueue import get_redis_settings

from . import settings as s
from . import spiders

setup()


# if "twisted.internet.reactor" in sys.modules:
#     del sys.modules["twisted.internet.reactor"]
# asyncioreactor.install()

# settings = get_project_settings()
settings = Settings({k: getattr(s, k) for k in dir(s) if not k.startswith("_")})
configure_logging(settings)


async def startup(ctx):
    f = open(os.path.join(os.path.dirname(__file__), "blacklists.json"))
    ctx["blacklists"] = json.loads(f.read())
    f.close()

    f = open(os.path.join(os.path.dirname(__file__), "domains.json"))
    ctx["domains"] = json.loads(f.read())
    f.close()


async def shutdown(ctx):
    pass


async def getSpider(ctx, url):
    tld = tldextract.extract(url)
    print(tld)
    # if tld.domain in ctx["blacklists"]["readability"] and tld.domain not in dir(
    #     ctx["domains"]
    # ):
    #     return spiders.generic.Spider
    getter = attrgetter(
        (ctx["domains"].get(tld.domain) or ctx["domains"].get("__default__") or {}).get(
            "spider", "generic"
        )
        + ".Spider"
    )
    return getter(spiders)


async def transformUrl(ctx, url):
    tld = tldextract.extract(url)
    return (
        (ctx["domains"].get(tld.domain) or ctx["domains"].get("__default__"))
        .get("transform", "{}")
        .format(url)
    )


def _nop(_):
    pass


# @wait_for(timeout=10)
async def _scrape(ctx, url, cb=_nop):
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
    redis_settings = get_redis_settings()
