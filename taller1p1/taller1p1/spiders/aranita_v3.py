#-*- coding:	utf-8 -*-
import scrapy

class QuotesSpider(scrapy.Spider):
	name = "aranita quotes v3"

	start_urls = [
		"http://quotes.toscrape.com/page/1"
	]		

	def parse(self, response):

		for quote in response.css('div.quote'):
			yield{
				'text'	:	quote.css('span.text::text').extract_first(),
				'author':	quote.css('small.text::text').extract_first(),
				'tags'	:	quote.css('div.tags a tag::text').extract()
			}
			self.log(quote.css('span.text::text').extract_first())