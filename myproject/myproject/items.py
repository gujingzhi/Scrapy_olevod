# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    intro = scrapy.Field()
    sort = scrapy.Field()
    type = scrapy.Field()
    year = scrapy.Field()
    link = scrapy.Field()
    picture = scrapy.Field()
    country = scrapy.Field()
    score = scrapy.Field()

