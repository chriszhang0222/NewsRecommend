import requests
from lxml import html
from pipeline.scraper.get_user_agent import random_user_agent

GET_CNN_NEWS_XPATH = """//p[contains(@class, 'zn-body__paragraph')]//text() | //div[contains(@class, 'zn-body__paragraph')]//text()"""
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
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
    except Exception as e:
        news = {}

    return news

print(extract_news('https://us.cnn.com/2020/09/15/health/us-coronavirus-tuesday/index.html'))