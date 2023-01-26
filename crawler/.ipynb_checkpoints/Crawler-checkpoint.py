import re, requests, bs4, json


class Crawler:

    def __init__(self, crawler_name):
        self.__crawler_name = crawler_name
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

    def _request_product_search(self, search_url):
        sess = requests.Session()
        sess.headers.update({'User-Agent': self.user_agent})
        sess.get(search_url)
        response = sess.get(search_url)

        return response, sess

    def search_and_append(self, item, num):
        pass

    def _sanitize_input(self, input):
        # remove special characters "&/\... etc"
        return re.sub('[^A-Za-z0-9]+', ' ', input)

    def _formatURL(self, base_url, item_name):
        return base_url.format(item_name)

    def _create_url(self, products_card):
        pass

    def _create_product_dto(self, product):
        pass


class Product_DTO:
    def __init__(self, product_price, product_name, product_url, full_info):
        self.price = product_price
        self.name = product_name
        self.url = product_url
        self.full_info = full_info
