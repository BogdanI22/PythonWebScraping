import scrapy

class ProductScraperSpiderSpider(scrapy.Spider):
    name = 'product_scraper_spider'
    allowed_domains = ["factorybuys.com.au"]
    start_urls = ["https://factorybuys.com.au/products"]

    def parse(self, response):
        collections = response.css('ul[class*=collection]')
        collection_item = collections.css('li')
        for item in collection_item:
            coll_link = item.css('h3 a::attr(href)').get()
            coll_link = "https://www.factorybuys.com.au" + coll_link
            yield response.follow(coll_link, callback=self.parse_collection_page)

    def parse_collection_page(self, response):
        # product_item = ProductFinderItem

        collections = response.css('ul[class*="product"]')
        collection_items = collections.css('li[class*="item"]')
        for item in collection_items:
            prices = item.css('.price-item::text').getall()
            yield {'name': item.css('h3 a::text').get(),
                   'url': item.css('h3 a::attr(href)').get(),
                   'collection': response.css('li[class*="breadcrumb"] a::attr(title)').get(),
                   'price_now': prices[1],
                   'price_old': prices[0]
                   }
