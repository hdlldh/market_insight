# -*- coding: utf-8 -*-
import scrapy
import datetime as dt
import pandas as pd


class YahooProfileSpider(scrapy.Spider):
    name = 'yahoo_profile'
    allowed_domains = ['yahoo.com']

    def __init__(self):
        symbols = pd.read_csv("market_insight/resources/symbol_list.csv")['Symbol']
        # example url: 'https://finance.yahoo.com/quote/T/profile?p=T'
        url_base = 'https://finance.yahoo.com/quote/%(sym)s/profile?p=%(sym)s'
        self.start_urls = [url_base % {'sym': symbol} for symbol in symbols]
        self.allowed_fields = ['Sector(s)', 'Industry', 'Full Time Employees']

    def parse(self, response):
        symbol = response.url.split('=')[-1]
        item = dict()
        pattern = '//div[contains(@class, "asset-profile-container")]//p[contains(@class, "D(ib) Va(t)")]//span//text()'
        spans = response.xpath(pattern)
        for i, span in enumerate(spans):
            txt = span.extract()
            if txt in self.allowed_fields:
                key = txt
                if i+1 < len(spans):
                    val = spans[i+1].extract()
                    if val is not None:
                        item[key] = val
                    else:
                        item[key] = ""
        if item:
            item['Symbol'] = symbol
            item['Timestamp'] = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return item
