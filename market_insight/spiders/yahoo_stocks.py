# -*- coding: utf-8 -*-
import scrapy
import datetime as dt
import pandas as pd
import json
import re
import requests
from market_insight.items import MarketInsightItem

class YahooStatisticsSpider(scrapy.Spider):
    name = 'yahoo_stocks'
    allowed_domains = ['yahoo.com']

    def __init__(self):
        symbols = pd.read_csv("market_insight/resources/symbol_list.csv")['Symbol']
        url_base = 'https://query1.finance.yahoo.com/v8/finance/chart'
        self.url_base2 = 'https://finance.yahoo.com/quote'
        self.start_urls = [f"{url_base}/{symbol}" for symbol in symbols]

    def parse(self, response):
        symbol = response.url.split('/')[-1]
        query = json.loads(response.text)
        quote = dict()
        try:
            quote['dataGranularity'] = query['chart']['result'][0]['meta']['dataGranularity']
            quote['tradingPeriods'] = query['chart']['result'][0]['meta']['tradingPeriods']
            quote['range'] = query['chart']['result'][0]['meta']['range']
            quote['timestamp'] = query['chart']['result'][0]['timestamp']
            quote['quote'] = query['chart']['result'][0]['indicators']['quote'][0]
        except KeyError or IndexError:
            pass

        item = MarketInsightItem()
        item['Symbol'] = symbol
        item['Timestamp'] = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['Quotes'] = quote

        url_base = 'https://finance.yahoo.com/quote'
        html = requests.get(url=f"{url_base}/{symbol}").text
        if "QuoteSummaryStore" not in html: return item

        json_str = html.split('root.App.main =')[1].split('(this)')[0].split(';\n}')[0].strip()
        data = json.loads(json_str)['context']['dispatcher']['stores']['QuoteSummaryStore']
        new_data = json.dumps(data).replace('{}', 'null')
        new_data = re.sub(r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)
        data_dict = json.loads(new_data)

        profile_dict = dict()
        if "summaryProfile" in data_dict:
            for field in ['sector','industry','fullTimeEmployees']:
                profile_dict[field] = data_dict["summaryProfile"].get(field, "")
        item['Profile'] = profile_dict
        item['Statistics'] = data_dict.get("defaultKeyStatistics", {})
        item['Financial'] = data_dict.get("financialData", {})
        item['Price'] = data_dict.get("price", {})
        item['Summary'] = data_dict.get("summaryDetail", {})
        item['Earnings'] = data_dict.get("earnings", {})
        item['Recommendation'] = data_dict.get("recommendationTrend", {})
        item['RateHistory'] = data_dict.get("upgradeDowngradeHistory", {})
        item['PageViews'] = data_dict.get("pageViews", {})
        return item
