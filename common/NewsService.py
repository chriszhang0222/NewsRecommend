import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

API_KEY = '6b8adb9bbe754e77b1291823b4715e92'
NEWS_API_ENDPOINT="https://newsapi.org/v2/everything"
NEWS_API_TOP = "https://newsapi.org/v2/top-headlines?"
NEWS_API_SOURCE = "https://newsapi.org/v2/sources"
DEFAULT_SOURCES = ['bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]


TOPICS = [
    'NBA', 'Trump', 'covid-19', 'bitcoin', 'US', 'Canada', 'Apple', 'Software',
    'coronavirus', 'Business', 'Technology', 'Entertainment', 'iPhone', 'iPad'
]
SORT_BY_TOP = 'top'
ARTICLES_API = "articles"

def getNewsWithSource():
    article = []
    params = {
        'apiKey': API_KEY,
    }
    payload = {
        **params,
        'sortBy': SORT_BY_TOP,
    }
    response = requests.get(NEWS_API_ENDPOINT, params=payload)
    res_json = json.loads(response.content.decode('utf-8'))
    if (res_json is not None and
            res_json['status'] == 'ok'):
        # populate news source in each articles
        for news in res_json['articles']:
            news['source'] = news['source']['name']

        article.extend(res_json['articles'])
    return article

def getNewsWithTopic(topics=TOPICS, sortBy=SORT_BY_TOP):
    params = {
        'apiKey': API_KEY,
    }

    def fetch_news(topic):
        article_local = []
        payload = {
            **params,
            'q': topic,
            'from': '2020-09-25',
            'sortBy': sortBy
        }
        response = requests.get(NEWS_API_ENDPOINT, params=payload)
        res_json = json.loads(response.content.decode('utf-8'))
        if (res_json is not None and
                res_json['status'] == 'ok'):
            # populate news source in each articles
            for news in res_json['articles']:
                news['source'] = news['source']['name']

            article_local.extend(res_json['articles'])
        return article_local

    articles = []
    with ThreadPoolExecutor(max_workers=16) as exe:
        tasks = [exe.submit(fetch_news, topic) for topic in topics]
        for future in as_completed(tasks):
            data = future.result()
            articles.extend(data)
    return articles

def getNewsFromSource(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):

    def fetch_news(source):
        article_local = []
        payload = {
            **params,
            'source': source,
            'sortBy': sortBy
        }
        response = requests.get(NEWS_API_ENDPOINT + ARTICLES_API, params=payload)
        res_json = json.loads(response.content.decode('utf-8'))
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # populate news source in each articles
            for news in res_json['articles']:
                news['source'] = res_json['source']

            article_local.extend(res_json['articles'])
        return article_local

    articles = []
    params = {
        'apiKey': API_KEY,
    }
    with ThreadPoolExecutor(max_workers=16) as exe:
        tasks = [exe.submit(fetch_news, source) for source in sources]
        for future in as_completed(tasks):
            data = future.result()
            articles.extend(data)
    return articles


def getNewsFromSource2(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = []

    for source in sources:
        payload = {'apiKey':API_KEY,
                   'source':source,
                   'sortBy':sortBy}

        response = requests.get(NEWS_API_ENDPOINT + ARTICLES_API, params=payload)
        res_json = json.loads(response.content.decode('utf-8'))

        # Extract info from response
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # populate news source in each articles
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])

    return articles


def fetch_news(topic):
    params = {
        'apiKey': API_KEY,
    }
    article_local = []
    payload = {
        **params,
        'q': topic,
        'from': '2020-09-01',
        'sortBy': 'publishedAt'
    }
    response = requests.get(NEWS_API_ENDPOINT, params=payload)
    res_json = json.loads(response.content.decode('utf-8'))
    if (res_json is not None and
        res_json['status'] == 'ok'):
        # populate news source in each articles
        for news in res_json['articles']:
            news['source'] = news['source']['name']

        article_local.extend(res_json['articles'])
    return article_local


