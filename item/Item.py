def mathBold_to_alphabet(char):
    if ord(char) >= 119808:
        try:
            if ord(char) >= 119834:
                # small letter
                return chr(ord(char) - 119737)
            else:
                return chr(ord(char) - 119743)
        except:
            return " "
    return char


class Search_Item:
    def __init__(self, search_name):
        self.item_name = search_name
        self.tesco_items = []
        self.aldi_items = []

    def __repr__(self):
        return """
        Search keyword: {}
        In Tesco basket, get {} item(s).
        In Aldi basket, get {} item(s).
        """.format(self.item_name, len(self.tesco_items), len(self.aldi_items))


class Item_Abstraction:
    def __init__(self, retailer_name, product_id,
                 product_name, product_page_url,
                 nutrition, selling_price, selling_volume, unit_price, unit_volume,
                 primary_category, second_category, third_category, full_info):
        self.retailer_name = retailer_name
        self.product_id = product_id
        self.product_name = product_name
        self.product_page_url = product_page_url
        self.nutrition = nutrition
        self.selling_price = selling_price
        self.selling_volume = selling_volume
        self.unit_price = unit_price
        self.unit_volume = unit_volume
        self.primary_category = primary_category
        self.second_category = second_category
        self.third_category = third_category
        self.full_info = full_info

    def __repr__(self):
        return """
        retailer name: {},
        product id: {},
        product name: {},
        product page_url: {},
        selling price: {}, 
        unit price: {},
        selling volume: {},
        category_1: {},
        category_2: {},
        category_3: {},
        product nutrition: {}
        """.format(self.retailer_name, self.product_id, self.product_name, self.product_page_url,
                   self.selling_price, self.unit_price, self.selling_volume, self.primary_category,
                   self.second_category, self.third_category, self.nutrition)


class Tesco_Item(Item_Abstraction):
    def __init__(self, retailer_name, product_id,
                 product_name, product_page_url,
                 nutrition, selling_price, selling_volume, unit_price, unit_volume,
                 primary_category, second_category, third_category, full_info):
        super().__init__(retailer_name="Tesco", product_id=product_id, product_name=product_name,
                         product_page_url=product_page_url,
                         nutrition=nutrition, selling_price=selling_price, selling_volume=selling_volume,
                         unit_price=unit_price, unit_volume=unit_volume,
                         primary_category=primary_category, second_category=second_category,
                         third_category=third_category,
                         full_info=full_info)


class Aldi_Item(Item_Abstraction):
    def __init__(self, retailer_name, product_id,
                 product_name, product_page_url,
                 nutrition, selling_price, selling_volume, unit_price, unit_volume,
                 primary_category, second_category, third_category, full_info):

        small_caps = ""
        for c in nutrition:
            small_caps = small_caps + mathBold_to_alphabet(c)

        nutrition = small_caps

        super().__init__(retailer_name="Aldi", product_id=product_id, product_name=product_name,
                         product_page_url=product_page_url,
                         nutrition=nutrition, selling_price=selling_price, selling_volume=selling_volume,
                         unit_price=unit_price, unit_volume=unit_volume,
                         primary_category=primary_category, second_category=second_category,
                         third_category=third_category,
                         full_info=full_info)
