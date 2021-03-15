import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from umweltbank.items import Article


class UmweltbankSpider(scrapy.Spider):
    name = 'umweltbank'
    start_urls = ['https://bankundumwelt.de/']

    def parse(self, response):
        links = response.xpath('//a[@class="post-link link"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="post-meta-date meta-info"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="post-content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
