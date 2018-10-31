import scrapy
from taller1p1.items import Taller1P1Item

class QuotesSpider(scrapy.Spider):
	name = "aranita quotes v5"

	start_urls = [
		"http://quotes.toscrape.com/page/1"
	]		

	def parse(self, response):

		for quote in response.css('div.quote'):

			yield Taller1P1Item(
				autor	=	quote.css('small.author::text').extract_first(),
				cita	=	quote.css('span.text::text').extract_first(),
				tags	=	quote.css('div.tags a.tag::text').extract()
			)

		next_url = response.css('li.next a ::attr(href)').extract_first()
		if next_url is not None:
			yield response.follow(next_url, callback=self.parse)