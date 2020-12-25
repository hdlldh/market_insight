# -*- coding: utf-8 -*-
import scrapy
import datetime as dt
import pandas as pd
import ujson as json
import re
import requests
from market_insight.items import MarketInsightItem

class YahooStatisticsSpider(scrapy.Spider):
    name = 'yahoo_stocks'
    allowed_domains = ['yahoo.com']

    def __init__(self):
        symbols = pd.read_csv("market_insight/resources/symbol_list.csv")['Symbol']
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

        item = MarketInsightItem()
        item['Symbol'] = symbol
        item['Timestamp'] = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
