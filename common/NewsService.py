import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = '6b8adb9bbe754e77b1291823b4715e92'
NEWS_API_ENDPOINT="https://newsapi.org/v1/"
DEFAULT_SOURCES = ['cnn']
SORT_BY_TOP = 'top'
ARTICLES_API = "articles"


def getNewsFronSource(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):

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
        return articles

    articles = []
    params = {
        'apiKey': API_KEY,
    }
    with ThreadPoolExecutor(max_workers=16) as exe:
        tasks = [exe.submit(fetch_news, source) for source in sources]
        for future in as_completed(tasks):
            data = future.result()
            articles.extend(data)
    return data

