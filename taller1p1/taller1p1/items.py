# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Taller1P1Item(scrapy.Item):
    autor	= scrapy.Field()
    cita 	= scrapy.Field()
    tags	= scrapy.Field()

#class Taller1P1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    pass
