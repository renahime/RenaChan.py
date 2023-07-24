from bs4 import BeautifulSoup
import requests
from .crawler_helpers import *
from .proxy import proxify
import re
from parsel import Selector
from urllib.parse import urljoin


def crawler_by_item_id(url, item_id):
    """
    Crawls a web page, extracts HTML elements by their 'id' attribute, and parses possible floating-point values.

    Parameters:
        url (str): The URL of the web page to crawl.
        item_id (str): The 'id' attribute value of the elements to find and extract.

    Returns:
        list: A list of parsed floating-point values extracted from the found HTML elements.

    Explanation:
    This function takes a URL (url) and a target 'id' attribute value (item_id) as input.
    It attempts to crawl the web page located at the given URL and fetches its HTML content using the get_html_content() function.
    If fetching the content fails, the function returns an error message.

    The function then uses find_elements_by_id() to find all HTML elements that have the specified 'id' attribute value.
    It extracts the text content from the found elements and stores them in the list 'possible_results'.

    Afterward, the function calls extract_floats_from_prices() to parse the possible floating-point values from 'possible_results'.
    It returns a list of parsed floating-point values.

    Note: This function relies on other helper functions (get_html_content, find_elements_by_id, extract_floats_from_prices)
    to perform specific tasks during the web crawling process.

    Example Usage:
        url = "https://www.example.com/products"
        item_id = "product_price"
        parsed_prices = crawler_by_item_id(url, item_id)
        if parsed_prices:
            print("Parsed Floating-Point Values:")
            for price in parsed_prices:
                print(price)
        else:
            print("No prices found or failed to fetch the content.")
    """
    try:
        html_content = get_html_content(url)
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch HTML content from {url}: {e}"

    elements = find_elements_by_id(html_content, item_id)

    possible_results = []
    for element in elements:
        possible_results.append(element.get_text())
    parsed_floats = extract_floats_from_prices(possible_results)
    return parsed_floats

def crawler_by_item_class(url, class_name):
    	# Headers for request
    try:
        html_content = get_html_content(url)
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch HTML content from {url}: {e}"
    elements = find_elements_by_class(html_content, class_name)

    print(elements)

def crawl_amazon(url, value, search_terms):
    # Headers for request
    try:
        response = requests.get(proxify(url))
        if response.status_code == 200:
            sel = Selector(text=response.text)
            optimal_product = 0
                ## Extract Product Data From Search Page
            search_products = sel.css("div.s-result-item[data-component-type=s-search-result]")
            optimal_product = {}
            for product in search_products:
                relative_url = product.css("h2>a::attr(href)").get()
                asin = relative_url.split('/')[3] if len(relative_url.split('/')) >= 4 else None
                product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
                if value < product.css(".a-price[data-a-size=xl] .a-offscreen::text").get():
                    optimal_product = product

            optimal_product={
                    "keyword": search_terms,
                    "asin": asin,
                    "url": product_url,
                    "ad": True if "/slredirect/" in product_url else False,
                    "title": product.css("h2>a>span::text").get(),
                    "price": product.css(".a-price[data-a-size=xl] .a-offscreen::text").get(),
                    "real_price": product.css(".a-price[data-a-size=b] .a-offscreen::text").get(),
                    "rating": (product.css("span[aria-label~=stars]::attr(aria-label)").re(r"(\d+\.*\d*) out") or [None])[0],
                    "rating_count": product.css("span[aria-label~=stars] + span::attr(aria-label)").get(),
                    "thumbnail_url": product.xpath("//img[has-class('s-image')]/@src").get(),
                }
    except Exception as e:
        print("Error", e)
        return None
