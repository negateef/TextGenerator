import os
from requests import get
from bs4 import BeautifulSoup
import urllib
import urllib2

books_url_template = "http://tululu.org/l82/{}/"
query_template = "http://tululu.org/txt.php?{}"
redirect_url = "http://tululu.org/"


# If overwrite = False, then no file will be downloaded if the folder exists
def download_corpus(folder_path='corpus/', overwrite=False, output=True):

    if output:
        print 'Download started!'

    folder_exists = os.path.exists(folder_path)
    if not overwrite and os.path.exists(folder_path):
        if output:
            print 'Cached version found. Download is completed!'
        return
    if not folder_exists:
        os.makedirs(folder_path)

    NUMBER_OF_PAGES = 20

    for pages in range(1, NUMBER_OF_PAGES + 1):
        req = get(books_url_template.format(pages))
        soup = BeautifulSoup(req.content.decode(req.encoding), "lxml")

        links = []
        for div in soup.findAll('div', attrs={'class': 'bookimage'}):
            link = div.find('a', href=True)
            links.append(link['href'])

        for link in links:
            book_id = link[2:-1]
            url = query_template.format(urllib.urlencode({'id': book_id}))

            # If there is no .txt version of a book
            if not is_redirect(url):
                path = folder_path + '/' + book_id + '.txt'
                download_file(url, path)
                decode_file(path)

        if output:
            print 'Progress: page {} out of {}'.format(pages, NUMBER_OF_PAGES)

    if output:
        print 'Download is completed!'


# Downloads a file from given url and saves it to path locally
def download_file(url, path):
    urllib.urlretrieve(url, path)


def decode_file(path, encoding='cp1251'):
    file_read = open(path, 'r')
    try:
        text = file_read.read().decode(encoding)
    except (UnicodeDecodeError, AttributeError) as exception:
        print 'Error occured while trying to decode {}'.format(path)
    file_read.close()

    file_write = open(path, 'w')
    file_write.write(text.encode('utf-8'))
    file_write.close()


def is_redirect(url):
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    final_url = res.geturl()
    if final_url == redirect_url:
        return True
    else:
        return False


def main():
    download_corpus(folder_path='corpus/', overwrite=False)

if __name__ == "__main__":
    main()
