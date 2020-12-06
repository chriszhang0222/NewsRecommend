import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

API_KEY = '6b8adb9bbe754e77b1291823b4715e92'
NEWS_API_ENDPOINT="https://newsapi.org/v2/everything"
NEWS_API_TOP = "https://newsapi.org/v2/top-headlines"
NEWS_API_SOURCE = "https://newsapi.org/v2/sources?language=en"
DEFAULT_SOURCES = [
    'yahoo-sports',
    'clutchpoints',
    'yahoo',
    'bbc',
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post',
    'abc-news,'
    'google-news',
    'google-news-ca',
    'cbc-news',
    'financial-post',
    'fox-news'
]


TOPICS = [
    "China",
    "NBA",
    "Marvel",
    "Disney+",
    "Trump",
    "Music",
    "MacBook",
    "iPhone",
    "iOS",
    "Apple",
    "covid-19",
    "american music awards",
    # "Redis",
    # "Kafka",
    # "MongoDB",
    # "ElasticSearch",
    # "Music",
    # "Movie",
    # "TV Show",
    # "Sports",
    "Soccer",
    "NFL",
    "Football",
    "F1",
    "Tennis",
    # "kim kardashian",
    # "Marvel Movies",
    "Justin Bieber"
    "Taylor Swift",
    "BlackPink"
    # "Javascript",
    # "Typescript",
    # "C++",
    # "Linux"
    # "Frontend Development",
    # "SpringCloud",
    # "Opensource",
    # "Github",
    # "SpringBoot",
    # "GoLang",
    # "Python",
    # "Java",
    # "Hadoop",
    # "Scala",
    # "Machine learning",
    # "Software Development",
    # "Amazon Web Service",
    # "Docker",
    # "Kubernetes",
    # "MicroService",
    # "Distributed System",
    # "Vue.js",
    # "React.js",
    # "Backend Development"
    # "Xi Jinping",
    # "Hong Kong"
    # 'NBA',
    # "Rajon Rondo",
    # "Lakers",
    # "76ers",
    # "kyrie irving"
    # "Houston Rockets",
    # "James Harden",
    # "Kevin Durant",
    # "Lebron James",
    # "Golden State Warriors",
    # "klay thompson",
    # "Stephen curry",
    # 'Trump', 'covid-19', 'bitcoin', 'US', 'Canada', 'Apple', 'Software'
    # , 'Business', 'Technology', 'Entertainment', "International", "Sports", "China",
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
            'language': 'en',
            # 'from': '2020-11-23',
            'sortBy': sortBy
        }
        response = requests.get(NEWS_API_ENDPOINT, params=payload)
        res_json = json.loads(response.content.decode('utf-8'))
        if (res_json is not None and
                res_json['status'] == 'ok'):
            # populate news source in each articles
            for news in res_json['articles']:
                news['source'] = news['source']['name']
                news['classify'] = topic

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
            'sources': source,
            'sortBy': sortBy
        }
        response = requests.get(NEWS_API_TOP, params=payload)
        res_json = json.loads(response.content.decode('utf-8'))
        if (res_json is not None and
            res_json['status'] == 'ok'):
            # populate news source in each articles
            for news in res_json['articles']:
                news['source'] = news['source']['name']

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


def fetch_news_top_us():
    params = {
        'apiKey': API_KEY,
    }
    article_local = []
    payload = {
        **params,
        'from': '2020-09-25',

    }
    response = requests.get(NEWS_API_TOP , params=payload)
    res_json = json.loads(response.content.decode('utf-8'))
    if (res_json is not None and
        res_json['status'] == 'ok'):
        # populate news source in each articles
        for news in res_json['articles']:
            news['source'] = news['source']['name']
            # news['classify'] = 'covid-19'

        article_local.extend(res_json['articles'])
    return article_local


fetch_news_top_us()