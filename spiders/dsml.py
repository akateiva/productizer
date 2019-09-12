# -*- coding: utf-8 -*-
import scrapy


class DsmlSpider(scrapy.Spider):
    name = 'dsml'
    allowed_domains = ['doverstreetmarket.com', 'shop.doverstreetmarket.com']
    #start_urls = ['https://shop.doverstreetmarket.com/t-shirt-space']
    start_urls = ['https://shop.doverstreetmarket.com/index']

    def parse(self, response):
        for href in response.css('.widget-category-link-inline a::attr(href)'):
            print(href)
            yield response.follow(href, self.parse_for_items)

    def parse_for_items(self, response):
        for item in response.css('li.item'):
            title = item.css('.product-name ::text').get()
            price = item.css('.price ::text').get()
            link = item.css('a::attr(href)').get()
            images = [item.css('img::attr(src)').get()]
            yield {'title': title,
                    'price': price,
                    'link': link,
                    'image_urls': images,
                    'mens': True,
                    'womens': True
                    }

        # follow pagination links
        for href in response.css('a.next::attr(href)'):
            yield response.follow(href, self.parse_for_items)
