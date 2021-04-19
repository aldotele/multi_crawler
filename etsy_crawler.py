from urllib.request import urlopen, Request
from html.parser import HTMLParser
import threading
import requests
import os
from datetime import datetime
import time


IMAGES_DIR = os.path.join(os.getcwd(), 'images')
STARTING_URL = 'https://www.etsy.com/it/search?q='


def ask_mode():  # sequential or multithread
    print('how do you want to run?\n1 - Sequential\n2 - Multithread')
    mode = input('Enter choice: ')
    while mode != '1' and mode != '2':
        mode = input('Not valid. Try again: ')
    return mode


def ask_products():
    queries = []
    query = input('which product? (leave blank to end): ')
    if not query:
        print('please enter at least one product.')
        quit()
    while query:
        queries.append(query)
        if len(queries) > 7:  # max 8 queries allowed
            break
        query = input('other products? (leave blank to end): ')
    print()
    mode = ask_mode()

    starting_time = time.time()

    if mode == '1':
        for q in queries:
            launch_thread(q)

    else:  # launch one thread per query
        threads = []
        for q in queries:
            t = threading.Thread(target=launch_thread, args=(q,))
            threads.append(t)
            t.start()  
        
        for t in threads:
            t.join()
    
    end_time = time.time()
    print('\nDone!')
    elapsed = end_time - starting_time
    print(f'the download took {elapsed} seconds')
          

def launch_thread(query):
    final_url = STARTING_URL + query
    url = Request(final_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
    except:
        print('product not found in Etsy!')
        quit()

    parser = MyHTMLParser()
    parser.links = []
    parser.feed(html)

    download_images(parser.links, query)


def download_images(links, name, date=str(datetime.now())[:-7]):
    date = date.replace(' ', '_')
    date = date.replace(':', '-')
    
    i = 1
    query_path = os.path.join(IMAGES_DIR, name, date)
    os.makedirs(query_path)
    for link in links:
        response = requests.get(link)
        image_name = f"{name}_{i}.png"
        p = os.path.join(query_path, image_name)
        file = open(p, "wb")
        file.write(response.content)
        file.close()
        i += 1


class MyHTMLParser(HTMLParser):
    links = []

    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            attrs = dict(attrs)
            if 'src' in attrs:
                self.links.append(attrs['src'])


def main():
    print('Welcome!\nEnter below the product images you want to download from Etsy.com')
    print()
    ask_products()


if __name__ == '__main__':
    main()

