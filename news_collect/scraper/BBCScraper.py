import requests
from lxml import html
from pipeline.scraper.get_user_agent import random_user_agent

GET_NEWS_XPATH = """//div[@class='css-83cqas-RichTextContainer e5tfeyi2']//text()"""
headers = {
    'Connection': 'close',
    'User-Agent': random_user_agent.get_user_agent()
}

def extract_news(news_url):
    """Extract news info"""
    # Fetch html
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=headers)
    news = {}
    try:
        tree = html.fromstring(response.content)
        news = tree.xpath(GET_NEWS_XPATH)
        news = ''.join(news)
    except Exception as e:
        news = {}

    return news

print(extract_news('https://www.bbc.com/news/av/world-asia-china-54157254'))