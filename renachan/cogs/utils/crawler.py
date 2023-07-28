import requests
from bs4 import BeautifulSoup, Tag
import re
import Levenshtein

class CreepyCrawler:
    def __init__(self, url, headers=None):
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3'
            }
        self.headers = headers
        self.url = url
        self.html_content = None

    def get_html_content(self):
        """
        Retrieves the HTML content from a given URL.

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
        # Headers for request
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        self.html_content = response.content
        return response.content

    def find_elements_by_id(self, html_content, item_id):
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


    def extract_floats_from_prices(self, prices):
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

    def find_elements_by_class(self, html_content, class_name):
        soup = BeautifulSoup(html_content, 'html.parser')
        elements = soup.find_all(class_=class_name)
        return elements

    def crawler_by_item_id(self, item_id):
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
            html_content = self.get_html_content()
        except requests.exceptions.RequestException as e:
            return f"Failed to fetch HTML content from {self.url}: {e}"

        elements = self.find_elements_by_id(html_content, item_id)

        possible_results = []
        for element in elements:
            possible_results.append(element.get_text())
        parsed_floats = self.extract_floats_from_prices(possible_results)
        return parsed_floats

    def crawler_by_item_class(self, class_name):
            # Headers for request
        try:
            html_content = self.get_html_content()
        except requests.exceptions.RequestException as e:
            return f"Failed to fetch HTML content from {self.url}: {e}"
        elements = self.find_elements_by_class(html_content, class_name)
        return elements

    def check_consecutive_match(self, tag_text, title_parts):
        # Check if the title parts appear consecutively in the tag's text
        if not tag_text.strip():
            return False

        tag_lower = tag_text.lower()
        last_index = 0
        for part in title_parts:
            part_lower = part.lower()
            index = tag_lower.find(part_lower, last_index)
            if index == -1:
                return False
            last_index = index + len(part_lower)
        return True

    def count_matching_words(self, tag_text, title_parts):
        # Count the number of matching words between tag_text and title_parts
        if not tag_text:
            return 0

        tag_words = tag_text.lower().split()
        title_words = [part.lower() for part in title_parts]
        return len(set(tag_words) & set(title_words))

    def find_title_in_siblings(self, sibling_tags, title):
        # Check for the title in the text of sibling tags and return the tag with the best similarity match
        best_match_tag = None
        best_match_distance = float('inf')

        for sibling in sibling_tags:
            sibling_classes = sibling.get('class', [])
            sibling_text = sibling.get_text()

            if not sibling_text.strip():
                continue

            distance = Levenshtein.distance(sibling_text, title)
            if distance < best_match_distance:
                best_match_tag = sibling
                best_match_distance = distance

        if best_match_tag:
            # print(f"Found closely similar title in sibling: {best_match_tag}")
            return best_match_tag

        return None

    def dfs_search(self, tag, visited_tags, path, title):
        if tag in visited_tags:
            return None

        # Check for the title in the current tag
        tag_text = tag.get_text()

        if not tag_text or not tag_text.strip():
            return None

        # print(f"CURRENT TAG: {tag.name}, Text: {tag_text}")
        distance = Levenshtein.distance(tag_text, title)

        if distance < 5:  # Adjust the threshold as needed
            # print(f"Found closely similar title in tag: {tag}")
            return tag, path

        # Check for the title in the current tag's siblings
        sibling_result = self.find_title_in_siblings(tag.find_next_siblings(), title)
        if sibling_result:
            return sibling_result, path

        # Check children tags
        for child in tag.children:
            if isinstance(child, Tag):
                child_result = self.dfs_search(child, visited_tags + [tag], path + [child], title)
                if child_result:
                    return child_result

        parent = tag.find_parent('div')
        if parent:
            return self.dfs_search(parent, visited_tags + [tag], path + [parent], title)

        return None

    def find_correct_element(self, class_name, title):
        """
        Find the element (tag) that shares the same div with the title.

        Parameters:
            class_name (list): The list of tags with the specified class name.
            title (str): The title to find.

        Returns:
            BeautifulSoup Tag or None: The element (tag) that shares the same div with the title, or None if not found.
        """

        for tag in class_name:
            result = self.dfs_search(tag, [], [tag], title)
            if result:
                return tag

        return None
    def extract_number_from_class(self, html_content_tag, currency):
        """
        Extract numbers with the specified currency symbol from the given HTML content tag.

        Parameters:
            html_content_tag (bs4.element.Tag): The HTML content tag.
            currency (str): The currency symbol associated with the numbers to extract (can be "¥" or "$").

        Returns:
            float or None: The matched number as a float, or None if no match is found.
        """
        if currency == "yen":
            return self.extract_number_before(html_content_tag, currency_symbol='円')
        elif currency == "$":
            return self.extract_number_after(html_content_tag, currency_symbol='$')
        else:
            raise ValueError("Invalid currency symbol. Supported symbols are '¥' and '$'.")

    def extract_number_before(self,html_content_tag, currency_symbol):
        """
        Extract numbers before the specified currency symbol from the given HTML content tag.

        Parameters:
            html_content_tag (bs4.element.Tag): The HTML content tag.
            currency_symbol (str): The currency symbol associated with the numbers to extract.

        Returns:
            float or None: The matched number as a float, or None if no match is found.
        """
        # Find the specific element that contains the price
        price_element = html_content_tag.find('span', class_='figure')
        if price_element is None:
            return None

        # Get the text content of the price element
        price_text = price_element.get_text(strip=True)

        # Remove commas and currency symbol, and convert to a float
        price_str = price_text.replace(',', '').replace(currency_symbol, '')
        try:
            matched_number = float(price_str)
            return matched_number
        except ValueError:
            return None
    def extract_number_after(self, html_content_tag, currency_symbol):
        """
        Extract numbers after the specified currency symbol from the given HTML content tag.

        Parameters:
            html_content_tag (bs4.element.Tag): The HTML content tag.
            currency_symbol (str): The currency symbol associated with the numbers to extract.

        Returns:
            float or None: The matched number as a float, or None if no match is found.
        """
        html_content = html_content_tag.get_text(strip=True)
        for part in html_content.split():
            if currency_symbol in part:
                # Remove commas and currency symbol, and convert to a float
                price_str = part.replace(',', '').replace(currency_symbol, '')
                try:
                    matched_number = float(price_str)
                    return matched_number
                except ValueError:
                    pass

        return None
