from bs4 import BeautifulSoup
import requests
from .crawler_helpers import *


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
