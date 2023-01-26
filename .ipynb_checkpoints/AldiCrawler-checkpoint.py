from crawler.Crawler import *


class AldiCrawler(Crawler):
    def __init__(self):
        super().__init__("Aldi_Crawler")
        self.base_url = "https://groceries.aldi.ie/en-GB/Search?keywords={}"

    def search_and_append(self, item_name, num):
        print(f'Start searching item: "{item_name}" at Aldi')
        
        # remove special characters "&/\... etc"
        item_name = Crawler.sanitize_input(input=item_name)

        return item_name