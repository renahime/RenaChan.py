import requests
from bs4 import BeautifulSoup
import re

def get_html_content(url):
    """
    Retrieves the HTML content from a given URL.

    Parameters:
        url (str): The URL from which to fetch the HTML content.

    Returns:
        bytes: The HTML content of the web page as bytes.

    Explanation:
    This function takes a URL (url) as input and retrieves the HTML content of the web page located at that URL.
    It uses the requests library to send an HTTP GET request to the URL and obtains the response. The response
    object contains the HTML content in its 'content' attribute, represented as bytes.

    The function raises an exception (requests.exceptions.HTTPError) for 4xx and 5xx status codes to indicate that
    there was an error while fetching the content.

    Note: The returned HTML content is in bytes format, and if you need it as a string, you can decode it using the
    appropriate encoding (e.g., 'utf-8').

    Example Usage:
        url = "https://www.example.com"
        try:
            html_content = get_html_content(url)
            decoded_content = html_content.decode('utf-8')
            print(decoded_content)
        except requests.exceptions.HTTPError as e:
            print(f"Error fetching the content: {e}")
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
    return response.content

def find_elements_by_id(html_content, item_id):
    """
    Finds HTML elements by their 'id' attribute in the given HTML content.

    Parameters:
        html_content (str): The HTML content as a string.
        item_id (str): The 'id' attribute value of the elements to find.

    Returns:
        list: A list of BeautifulSoup Tag objects representing the elements found with the given 'id'.

    Explanation:
    This function takes the HTML content as a string (html_content) and a target 'id' attribute value (item_id) as input.
    It then uses BeautifulSoup to parse the HTML content and find all elements that have the specified 'id' attribute value.
    The function returns a list of BeautifulSoup Tag objects representing the found elements.

    Note: BeautifulSoup is a popular Python library for parsing HTML and XML documents.

    Example Usage:
        html_content = '<div id="element1">...</div><p id="element2">...</p>'
        item_id = "element1"
        elements = find_elements_by_id(html_content, item_id)
        if elements:
            for element in elements:
                print(element)
        else:
            print("No elements found with the specified 'id'.")
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(id=item_id)
    return elements

def extract_floats_from_prices(prices):
    """
    Extracts floating-point numbers from a list of price data containing Japanese text.

    Parameters:
        prices (list of str): A list of strings containing price data in Japanese text.

    Returns:
        list of float: A list of extracted floating-point numbers from the price data.

    Explanation:
    This function takes a list of strings (prices) as input, where each string contains
    price data in Japanese text. It then extracts the floating-point numbers from each
    string and returns them as a list of float values.

    The function works as follows:

    1. Create an empty list 'extracted_floats' to store the extracted floating-point numbers.

    2. Define a regular expression pattern 'pattern' to match numeric values in the Japanese text.
       The pattern [0-9]+(?:[,.][0-9]+)? will match numbers with optional commas or periods as decimal separators.

    3. Iterate through each element 'price_data' in the 'prices' list.

        a. Use regular expression 'findall' method to find all numeric values in the Japanese text
           based on the defined 'pattern'. The result is stored in the 'numeric_values' list.

        b. For each 'value' in 'numeric_values', remove commas (if present) from the numeric value
           and convert it to a floating-point number using the 'float' function.

        c. Append the extracted float value to the 'extracted_floats' list.

    4. After processing all price data in the 'prices' list, return the 'extracted_floats' list
       containing all the extracted floating-point numbers.
    """
    extracted_floats = []

    # Regular expression to match numeric values in the Japanese text
    pattern = r'[0-9]+(?:[,.][0-9]+)?'

    for price_data in prices:
        # Use regex to find all numeric values in the Japanese text
        numeric_values = re.findall(pattern, price_data)

        for value in numeric_values:
            # Remove commas from numeric value and convert it to a float
            value = float(value.replace(',', ''))
            extracted_floats.append(value)

    return extracted_floats
