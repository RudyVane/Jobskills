import scrapy
from readability import Document
from bs4 import BeautifulSoup

class ReadabilitySpider(scrapy.Spider):
    name = "readability"
    def parse(self, response):
        doc = Document(response.text)
        
        yield {
            "url": response.css('link[rel="canonical"]::attr(href)').get() or response.url,
            "lang": response.css('html::attr(lang)').get() or "en", #default to english?
            "title": doc.title(),
            "text": BeautifulSoup(doc.summary()).get_text()
        }