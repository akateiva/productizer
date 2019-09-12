# -*- coding: utf-8 -*-
import scrapy


class GoodhoodSpider(scrapy.Spider):
    name = 'goodhood'
    allowed_domains = ['goodhoodstore.com']
    start_urls = ['https://goodhoodstore.com/mens/all-mens-clothing', 'https://goodhoodstore.com/mens/all-mens-footwear']

    def parse(self, response):
        for item in response.css('ul.Products-List>li>div.overview'):
            data = {}
            data['product_name'] = item.css('.Title ::text').get()
            data['brand'] = item.css('.Brand ::text').get()
            data['price'] = item.css('.Price ::text').get()
            data['link'] = response.urljoin(item.css('a::attr(href)').get())
            data['sizes'] = item.css('.Types>.In-Stock::text').extract()
            data['image_urls'] = ['https:' + item.css('img::attr(src)').get()]
            data['mens'] = True
            data['womens'] = False
            yield data
        
        # follow pagination
        for href in response.css('a[rel=next]::attr(href)'):
            yield response.follow(href, self.parse)
