# -*- coding: utf-8 -*-
import scrapy
from taller1p2.items import Taller1P2Item

class InfSpider(scrapy.Spider):
	name = 'InfSpider'
	#allowed_domains = ['inf.ucv.cl/']
	start_urls = ['http://www.inf.ucv.cl/']

	def parse(self, response):
		hxs = scrapy.Selector(response)
		all_links = hxs.xpath('*//a/@href').extract()

		for link in all_links:

			if link.encode("utf-8") != "#":
				if (link.startswith('http://') or link.startswith('https://')) :
					#print link.encode("utf-8")
					#self.start_urls.append(link.encode("utf-8"))
					yield scrapy.Request(link.encode("utf-8"), method='HEAD', callback=self.urlInfo, meta={ 'dont_retry': True, 'handle_httpstatus_list': [302]}, dont_filter = True )
	
	def urlInfo(self, response):

		if response.headers['Content-Type'] in "text/html":

			if response.headers.get('Content-Length') is None:

				yield Taller1P2Item(
					URL = response.url,
					status = response.status,
					content_type = response.headers['Content-Type'],
					content_length = 0
					#content_length = int(response.headers['Content-Length'])
				)

			elif response.headers.get('Content-Length') is not None:

				yield Taller1P2Item(
					URL = response.url,
					status = response.status,
					content_type = response.headers['Content-Type'],	
					content_length = int(response.headers['Content-Length'])
				)