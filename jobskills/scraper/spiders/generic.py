import scrapy
from bs4 import BeautifulSoup


class GenericSpider(scrapy.Spider):
    name = "generic"

    def parse(self, response):
        yield {
            "url": response.css('link[rel="canonical"]::attr(href)').get()
            or response.url,
            "lang": response.css("html::attr(lang)").get(),
            "title": BeautifulSoup(response.css("title").get()).get_text(),
            "text": BeautifulSoup(response.css("body").get()).get_text(),
        }
