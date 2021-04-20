from html.parser import HTMLParser
import os
from urllib.request import urlopen, Request
import requests
from crawler.helper import custom_datetime


IMAGES_DIR = os.path.join(os.getcwd(), 'images')
STARTING_URL = 'https://www.etsy.com/it/search?q='


class EtsyCrawler(HTMLParser):
    links = []

    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            attrs = dict(attrs)  # key is the tag attribute and value is its value
            if 'src' in attrs:
                self.links.append(attrs['src'])


class ImgDownloader:
    @staticmethod
    def download_images(links, name, date=custom_datetime()):
        i = 1
        query_path = os.path.join(IMAGES_DIR, name, date)
        os.makedirs(query_path)  # creating a folder for each query with sub-folder for each datetime
        for link in links:
            response = requests.get(link)
            image_name = f"{name}_{i}.png"
            p = os.path.join(query_path, image_name)
            file = open(p, "wb")
            file.write(response.content)
            file.close()
            i += 1


def parse_and_download(query):
    final_url = STARTING_URL + query
    url = Request(final_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
    except:
        print('product not found on Etsy!')
        quit()

    parser = EtsyCrawler()
    EtsyCrawler.links = []
    parser.feed(html)
    ImgDownloader.download_images(parser.links, query)
