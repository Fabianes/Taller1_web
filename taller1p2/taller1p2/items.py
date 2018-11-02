# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Taller1P2Item(scrapy.Item):
	URL = scrapy.Field()
	status = scrapy.Field()
	content_type = scrapy.Field()
	content_length = scrapy.Field()