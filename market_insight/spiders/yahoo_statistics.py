# -*- coding: utf-8 -*-
import scrapy
import datetime as dt
import pandas as pd
import ujson as json
import re
import requests

class YahooStatisticsSpider(scrapy.Spider):
    name = 'yahoo_statistics'
    allowed_domains = ['yahoo.com']

    def __init__(self):
        symbols = pd.read_csv("market_insight/resources/symbol_list.csv")['Symbol']
        # example url: 'https://finance.yahoo.com/quote/MSFT/key-statistics?p=MSFT'
        url_base = 'https://finance.yahoo.com/quote'
        self.start_urls = [f"{url_base}/{symbol}" for symbol in symbols]

    def parse(self, response):
        symbol = response.url.split('/')[-1]
        html = response.text
        if "QuoteSummaryStore" not in html:
            html = requests.get(url=response.url).text
            if "QuoteSummaryStore" not in html:
                return

        json_str = html.split('root.App.main =')[1].split('(this)')[0].split(';\n}')[0].strip()
        data = json.loads(json_str)['context']['dispatcher']['stores']['QuoteSummaryStore']
        new_data = json.dumps(data).replace('{}', 'null')
        new_data = re.sub(r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)
        data_dict = json.loads(new_data)
        fields = ['summaryProfile', 'summaryDetail', 'quoteType',
                 'defaultKeyStatistics', 'assetProfile', 'summaryDetail']
        item = dict()
        for field in fields:
            if isinstance(data_dict.get(field), dict):
                item.update(data_dict[field])

        blacklist = ["longBusinessSummary", "city", "phone", "state", "country", "companyOfficers",
                     "website",	"address1", "fax", "zip", "maxAge", "toCurrency",
                     "expireDate", "yield", "algorithm", "circulatingSupply",
                     "startDate", "lastMarket", "maxSupply", "openInterest",
                     "volumeAllCurrencies", "strikePrice", "ytdReturn", "fromCurrency",
                     "longName", "exchangeTimezoneName", "exchangeTimezoneShortName",
                     "isEsgPopulated", "gmtOffSetMilliseconds", "messageBoardId", "market",
                     "annualHoldingsTurnover", "morningStarRiskRating", "lastSplitFactor",
                     "legalType", "morningStarOverallRating", "impliedSharesOutstanding",
                     "category", "symbol"]

        for field in blacklist:
            if field in item:
                item.pop(field)

        if item:
            item['Symbol'] = symbol
            item['Timestamp'] = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return item

