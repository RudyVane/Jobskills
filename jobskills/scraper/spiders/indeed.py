import scrapy
from bs4 import BeautifulSoup


class Spider(scrapy.Spider):
    name = "indeed"

    def parse(self, response):
        print("Started parse in IndeedSpider")
        text = BeautifulSoup(
            response.css("div.jobsearch-JobComponent").get(), "html.parser"
        )
        text.find("div", {"id", "jobsearch-ViewJobButtons-container"}).decompose()
        text.find("div", {"class", "jobsearch-JobMetadataFooter"}).decompose()

        yield {
            "url": response.css('link[rel="canonical"]::attr(href)').get(),
            "lang": response.css("h1.jobsearch-JobInfoHeader-title::attr(lang)").get(),
            "title": BeautifulSoup(
                response.css("h1.jobsearch-JobInfoHeader-title").get(), "html.parser"
            ).get_text(),
            "text": text.get_text(),
        }
