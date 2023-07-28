import scrapy
from bs4 import BeautifulSoup

class IndeedSpider(scrapy.Spider):
    name = "indeed"
    allowed_domains = ["indeed.com", "indeed.nl"]

    def parse(self, response):
        text = BeautifulSoup(response.css('div.jobsearch-JobComponent').get(), 'html.parser')
        text.find("div", {"id","jobsearch-ViewJobButtons-container"}).decompose()
        
        yield {
            "url": response.css('link[rel="canonical"]::attr(href)').get(),
            "lang": response.css('h1.jobsearch-JobInfoHeader-title::attr(lang)').get(),
            "title": BeautifulSoup(response.css('h1.jobsearch-JobInfoHeader-title').get(), 'html.parser').get_text(),
            "text" : text.get_text()
        }
