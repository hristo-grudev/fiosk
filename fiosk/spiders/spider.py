import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import FioskItem
from itemloaders.processors import TakeFirst


class FioskSpider(scrapy.Spider):
	name = 'fiosk'
	start_urls = ['https://www.fio.sk/o-nas/media/tlacove-spravy']

	def parse(self, response):
		post_links = response.xpath('//h6/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="paginator"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="section3 newsSection"]//text()[normalize-space() and not(ancestor::p[@class="meta"])]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="meta"]/text()').get()

		item = ItemLoader(item=FioskItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
