from crawler.Crawler import *
from item.Item import *


class TescoCrawler(Crawler):
    def __init__(self):
        super().__init__("Tesco_Crawler")
        self.__host_name = 'https://www.tesco.ie'
        self.__base_url = "https://www.tesco.ie/groceries/en-IE/search?query={}"
        self.__product_base_url = "https://www.tesco.ie/groceries/en-IE/products/"

    def search_and_append(self, item, num):
        # item: search item
        # num: search through how many products in the result page

        print(f'Start searching item: "{item.item_name}" at Tesco')

        # create search URL
        item.item_name = self._sanitize_input(item.item_name)
        search_url = super()._formatURL(self.__base_url, item.item_name)

        # make request to search for related products
        (search_response, session) = super()._request_product_search(search_url)

        # parse
        url_to_crawl = self.__create_urls(search_response, num)

        items = self.__get_product_detail(url_to_crawl, session)

        # add to search_item
        item.tesco_items = items

        return item

    def __get_product_detail(self, url_to_crawl, session):

        basket = []

        for num in range(len(url_to_crawl)):
            print(f"looking into {url_to_crawl[num]}")
            response = session.get(url_to_crawl[num])
            print(f"response: {response.status_code}")

            aldi_item = self._parse_product_landing_page(response)
            basket.append(aldi_item)

        return basket

    def _parse_product_landing_page(self, response):
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        item = soup.find(id='data-attributes')
        raw_json = item['data-redux-state']
        spec_dict = json.loads(raw_json)

        tesco_item = Tesco_Item(
            retailer_name="Tesco",
            product_id=spec_dict['productDetails']['item']['product']['gtin'],
            product_name=spec_dict['productDetails']['item']['product']['title'],
            product_page_url=response.url,
            nutrition=spec_dict['productDetails']['item']['product']['details']['nutritionInfo'],
            selling_price=spec_dict['productDetails']['item']['product']['price'],
            selling_volume=spec_dict['productDetails']['item']['product']['details']['packSize'],
            unit_price=spec_dict['productDetails']['item']['product']['unitPrice'],
            unit_volume=spec_dict['productDetails']['item']['product']['unitOfMeasure'],
            primary_category=spec_dict['productDetails']['item']['product']['superDepartmentName'],
            second_category=spec_dict['productDetails']['item']['product']['departmentName'],
            third_category=spec_dict['productDetails']['item']['product']['aisleName'],
            full_info=spec_dict['productDetails']['item']['product'])
        return tesco_item

    def __create_urls(self, response, num):
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        element = soup.find(id='data-attributes')
        raw_json = element['data-redux-state']
        items_card_dict = json.loads(raw_json)
        items = items_card_dict['results']['pages'][0]['serializedData']

        url_list = []

        if len(items) > num:
            for n in range(num):
                product = items[n]
                product_id = product[0]
                url_list.append("{}{}".format(self.__product_base_url, product_id))
        else:
            for n in range(len(items)):
                product = items[n]
                product_id = product[0]
                url_list.append("{}{}".format(self.__product_base_url, product_id))

        return url_list
