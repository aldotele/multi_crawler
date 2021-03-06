import threading
import time
from crawler.crawler import parse_and_download
from crawler.crawler_handler import ask_mode, ask_products


def main():
    print('Welcome!\nEnter below the product images you want to download from Etsy.com')
    print()
    queries = ask_products()
    print()
    mode = ask_mode()  # mode can be either sequential or multi-thread

    starting_time = time.time()

    if mode == '1':  # sequential mode chosen
        for q in queries:
            parse_and_download(q)
    else:  # multi-thread chosen: launching one thread per query
        threads = []
        for q in queries:
            t = threading.Thread(target=parse_and_download, args=(q,))
            threads.append(t)
            t.start()  

        # waiting for all threads to complete
        for t in threads:
            t.join()

    end_time = time.time()
    print('\nDone!')
    # showing how much time it took to download everything
    elapsed = end_time - starting_time
    print(f'the download took {elapsed} seconds')


if __name__ == '__main__':
    main()

