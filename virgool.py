import requests
from io import BytesIO
from bs4 import BeautifulSoup as Soup

from cfscraper import CfScraper


class Virgool(CfScraper):
    """ Virgool Post """
    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post = Soup(self.scraper.get(url).content, 'html5lib')

    def get_title(self):
        return self.post.find('div', attrs={'class': 'post-content'}).h1.text

    def get_name(self):
        return self.post.find('a', attrs={'class': 'module--name'}).text[1:-1]

    def get_bio(self):
        return self.post.find('p', attrs={'class': 'module--bio'}).text

    def get_avatar(self):
        src = self.post.find('div', attrs={'class': 'module--avatar'}).img['src']
        return BytesIO(self.scraper.get(src).content)

    def get_username(self):
        return self.post.find('div', attrs={'class': 'module--avatar'}).a['href'][19:]

    def get_poster(self):
        src = self.post.find('div', attrs={'class': 'post-body'}).img['src']
        return BytesIO(self.scraper.get(src).content)
