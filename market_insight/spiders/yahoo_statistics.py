# -*- coding: utf-8 -*-
import scrapy
import datetime as dt
import pandas as pd


class YahooStatisticsSpider(scrapy.Spider):
    name = 'yahoo_statistics'
    allowed_domains = ['yahoo.com']

    def __init__(self):
        symbols = pd.read_csv("market_insight/resources/symbol_list.csv")['Symbol']
        # example url: 'https://finance.yahoo.com/quote/MSFT/key-statistics?p=MSFT'
        url_base = 'https://finance.yahoo.com/quote/%(sym)s/key-statistics?p=%(sym)s'
        self.start_urls = [url_base % {'sym': symbol} for symbol in symbols]

    def parse(self, response):
        symbol = response.url.split('=')[-1]
        item = dict()
        item['Symbol'] = symbol
        xpath_base0 = '//div[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div[1]/div/table/tbody/tr[%s]/td[%s]//text()'
        xpath_base1 = '//div[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div[2]/div[%s]/table/tbody/tr[%s]/td[%s]//text()'
        xpath_base2 = '//div[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[%s]/table/tbody/tr[%s]/td[%s]//text()'
        for tr_ix in range(1, 10):
            name = response.xpath(xpath_base0 % (tr_ix, 1)).extract_first()
            value = response.xpath(xpath_base0 % (tr_ix, 2)).extract_first()
            if name:
                name = name.strip()
                item[name] = value.strip()
        for div_ix in range(1, 10):
            for tr_ix in range(1, 10):
                name = response.xpath(xpath_base1 % (div_ix, tr_ix, 1)).extract_first()
                value = response.xpath(xpath_base1 % (div_ix, tr_ix, 2)).extract_first()
                if name:
                    name = name.strip()
                    item[name] = value.strip()

                name = response.xpath(xpath_base2 % (div_ix, tr_ix, 1)).extract_first()
                value = response.xpath(xpath_base2 % (div_ix, tr_ix, 2)).extract_first()
                if name:
                    name = name.strip()
                    item[name] = value.strip()
        item['Timestamp'] = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return item
