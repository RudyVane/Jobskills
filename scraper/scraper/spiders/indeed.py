import scrapy
from bs4 import BeautifulSoup

def process_text(response):
    res = BeautifulSoup(response.css('div.jobsearch-JobComponent').get(), 'html.parser')
    res.find("div", {"id","jobsearch-ViewJobButtons-container"}).decompose()
    return res.get_text()

class IndeedSpider(scrapy.Spider):
    name = "indeed"
    allowed_domains = ["indeed.com", "indeed.nl"]
    # url_list = ["https://nl.indeed.com/viewjob?jk=5b494d31c319e0d6"]

    # HEADERS = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    #     "Accept-Language": "en-US,en;q=0.5",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Connection": "keep-alive",
    #     "Upgrade-Insecure-Requests": "1",
    #     "Sec-Fetch-Dest": "document",
    #     "Sec-Fetch-Mode": "navigate",
    #     "Sec-Fetch-Site": "none",
    #     "Sec-Fetch-User": "?1",
    #     "Cache-Control": "max-age=0",
    # }

    # def start_requests(self):
    #     for url in self.url_list:
    #         yield scrapy.Request(url="https://webcache.googleusercontent.com/search?q=cache:"+url, callback=self.parse)#, headers=self.HEADERS)

    def parse(self, response):
        yield {
            "url": response.css('link[rel="canonical"]::attr(href)').get(),
            "lang": response.css('h1.jobsearch-JobInfoHeader-title::attr(lang)').get(),
            "title": BeautifulSoup(response.css('h1.jobsearch-JobInfoHeader-title').get(), 'html.parser').get_text(),
            "text" : process_text(response)
        }
