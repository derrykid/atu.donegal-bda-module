import re

class Crawler:
    def __init__(self, crawler_name):
        self.crawler_name = crawler_name

    def search_and_append(self, item, num):
        pass
    
    def sanitize_input(self, input):
        return re.sub('[^A-Za-z0-9]+', ' ', input)
