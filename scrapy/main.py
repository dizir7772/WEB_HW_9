from datetime import datetime
from multiprocessing import Process

import scrapy
from scrapy.crawler import CrawlerProcess


class ISpider(scrapy.Spider):
    pass


class AuthorsSpider(ISpider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": 'utf-8',
        "FEED_URI": f"authors.json"
    }

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get(),
                                  callback=self.parse_author)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        content = response.xpath("/html//div[@class='author-details']")
        yield {
            "fullname": content.xpath("h3/text()").get().strip().replace("-", " "),
            "born_date": content.xpath("p/span[@class='author-born-date']/text()").get().strip(),
            "born_location": content.xpath("p/span[@class='author-born-location']/text()").get().strip(),
            "description": content.xpath("div[@class='author-description']/text()").get().strip(),
        }


class QuotesSpider(ISpider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": 'utf-8',
        "FEED_URI": f"quotes.json"
    }

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "quote": quote.xpath("span[@class='text']/text()").get(),
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


def run_spider(entity: ISpider):
    process = CrawlerProcess()
    process.crawl(entity)
    process.start()


if __name__ == '__main__':

    pr1 = Process(target=run_spider, args=(QuotesSpider, ))
    pr2 = Process(target=run_spider, args=(AuthorsSpider,))
    pr1.start()
    pr2.start()
    pr1.join()
    pr2.join()