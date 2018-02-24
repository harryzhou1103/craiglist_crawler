# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['sfbay.craigslist.org']
    start_urls = ['http://sfbay.craigslist.org/search/egr']

    def parse(self, response):
        listings = response.xpath('//li[@class="result-row"]')
        for listing in listings:
            date = listing.xpath('.//time[@class="result-date"]/@datetime').extract_first()
            link = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
            text = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()

            yield {"date" : date,
                   "link" : link,
                   "text" : text,
                  }

            next = response.xpath('//a[@class="button next"]/@href').extract_first()
            if next:
                yield scrapy.Request(response.urljoin(next), callback=self.parse)

