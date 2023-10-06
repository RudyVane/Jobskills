import scrapy
from bs4 import BeautifulSoup


class Spider(scrapy.Spider):
    name = "generic"

    def parse(self, response):
        yield {
            "url": response.css('link[rel="canonical"]::attr(href)').get()
            or response.url,
            "lang": response.css("html::attr(lang)").get(),
            "title": BeautifulSoup(response.css("title").get(), "lxml").get_text(),
            "text": BeautifulSoup(response.css("body").get(), "lxml").get_text(),
        }
