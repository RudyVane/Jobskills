import scrapy
from bs4 import BeautifulSoup
from readability import Document


class Spider(scrapy.Spider):
    name = "readability"

    def parse(self, response):
        print("Started readability spider parse")
        doc = Document(response.text)

        yield {
            "url": response.css('link[rel="canonical"]::attr(href)').get()
            or response.url,
            "lang": response.css("html::attr(lang)").get()
            or "en",  # default to english?
            "title": doc.title(),
            "text": BeautifulSoup(doc.summary(), "lxml").get_text(),
        }
