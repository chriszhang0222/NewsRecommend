import requests
import json
from pipeline.scraper.get_user_agent import random_user_agent
from lxml import html, etree

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Connection": "close",
}
news_url = 'https://www.bbc.com/news/world-middle-east-54168120'

session = requests.session()
response = session.get(news_url, headers=headers)
xpath_string = """//p[contains(@class, 'zn-body__paragraph')]//text() | //div[contains(@class, 'zn-body__paragraph')]//text()"""
