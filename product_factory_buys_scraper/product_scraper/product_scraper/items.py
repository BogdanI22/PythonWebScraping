# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductScraperItem(scrapy.Item):
    # define the fields for your item here like:
    #name = scrapy.Field()
    pass

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    collection = scrapy.Field()
    url = scrapy.Field()
    price_now = scrapy.Field()
    price_old = scrapy.Field()
