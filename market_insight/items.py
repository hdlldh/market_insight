# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import json


class MarketInsightItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Symbol = scrapy.Field()
    Timestamp = scrapy.Field()
    Profile = scrapy.Field(serializer=lambda x:json.dumps(x))
    Statistics = scrapy.Field(serializer=lambda x: json.dumps(x))
    Financial = scrapy.Field(serializer=lambda x: json.dumps(x))
    Price = scrapy.Field(serializer=lambda x: json.dumps(x))
    Summary = scrapy.Field(serializer=lambda x: json.dumps(x))
    Earnings = scrapy.Field(serializer=lambda x: json.dumps(x))
    Recommendation = scrapy.Field(serializer=lambda x: json.dumps(x))
    RateHistory = scrapy.Field(serializer=lambda x: json.dumps(x))
    PageViews = scrapy.Field(serializer=lambda x: json.dumps(x))


