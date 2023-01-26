from carwler.Crawler import *
from item.Item import *


class AldiCrawler(Crawler):
    def __init__(self):
        super().__init__("Aldi_Crawler")
        self.__host_name = 'https://groceries.aldi.ie'
        self.__base_url = "https://groceries.aldi.ie/en-GB/Search?keywords={}"
        self.__search_result_css_selector = 'div[data-oc-controller="Product.SearchSummary"]'

    def search_and_append(self, item, num):
        # item: target item
        # num: search through how many products in the result page

        print(f'Start searching item: "{item.item_name}" at Aldi')

        # create search URL
        item.item_name = self._sanitize_input(item.item_name)
        search_url = super()._formatURL(self.__base_url, item.item_name)

        # make request to search for related products
        (search_response, session) = super()._request_product_search(search_url)

        # parse
        product_dto_list = self._parse_product_card(search_response, num,
                                                    css_selector=self.__search_result_css_selector)
        url_to_crawl = self._create_url(product_dto_list)
        items = self.__get_product_detail(url_to_crawl, product_dto_list, session)

        # add to search_item
        item.aldi_items = items

        return item

    def __get_product_detail(self, url_to_crawl, product_dto_list, session):

        basket = []

        for num in range(len(url_to_crawl)):
            print(f"looking into {url_to_crawl[num]}")
            response = session.get(url_to_crawl[num])
            print(f"response: {response.status_code}")
            aldi_item = self._parse_product_landing_page(response, product_dto_list[num])
            basket.append(aldi_item)

        return basket

    def _parse_product_landing_page(self, response, product_dto):
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        item = soup.find(id='product-summary')
        raw_json = item['data-context']
        spec_dict = json.loads(raw_json)

        nutrition_facts = self.__get_nutrition(soup)

        aldi_item = Aldi_Item(
            retailer_name="Aldi",
            product_id=spec_dict['productId'],
            product_name=spec_dict['DisplayName'],
            product_page_url=response.url,
            nutrition=nutrition_facts,

            selling_price=product_dto.price,
            selling_volume=spec_dict['SizeVolume'],
            unit_price=0,
            unit_volume=0,

            primary_category=spec_dict['PrimaryCategoryName'], second_category=spec_dict['SecondaryCategoryName'],
            third_category=spec_dict['TertiaryCategoryName'], full_info=spec_dict
        )
        return aldi_item

    def __get_nutrition(self, soup):
        talbes = soup.findAll('table', class_="table table-striped")
        td = talbes[0].findAll('td')
        return td[1].text

    def _create_url(self, products_card):
        results = []
        for e in products_card:
            results.append(f"{self.__host_name}{e.url}")

        return results

    def _create_product_dto(self, product):
        product_price = product['ListPrice']
        product_name = product['FullDisplayName']
        product_url = product['Url']
        return Product_DTO(product_price, product_name, product_url, product)

    def _parse_product_card(self, response, num, css_selector):

        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        items = soup.select(css_selector)

        product_dto_list = []

        if items:
            item = items[0]  # first item
            raw_json = item['data-context']
            attribute_dict = json.loads(raw_json)
            products_list = attribute_dict['SearchResults']

            if len(products_list) > num:
                for n in range(num):
                    x = self._create_product_dto(products_list[n])
                    product_dto_list.append(x)

            else:
                for n in range(len(products_list)):
                    obj = self._create_product_dto(products_list[n])
                    product_dto_list.append(obj)

        return product_dto_list
