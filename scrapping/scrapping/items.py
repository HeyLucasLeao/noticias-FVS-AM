# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrappingItem(scrapy.Item):
    # define the fields for your item here like:
    titulo = scrapy.Field()
    data = scrapy.Field()
    link = scrapy.Field()
