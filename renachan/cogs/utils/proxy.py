import requests
from parsel import Selector
from urllib.parse import urlencode, urljoin

API_KEY = '8deea6bb-484e-4241-88ac-953f6e096b1f'

def proxify(url):
    payload = {'api_key': API_KEY, 'url': url, 'country': 'us'}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url
