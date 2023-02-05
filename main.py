import os
import time
import textwrap
import argparse
import logging
from urllib.parse import urljoin, urlsplit

import requests

from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup


def download_txt(url, filename, folder='books'):
    """Функция для скачивания текстовых файлов.

    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.

    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    params = {
        'id': filename.split('/')[0],
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)

    name = f"{sanitize_filename(filename)}"
    path = f'{os.getcwd()}/{folder}/{name}.txt'
    with open(path, 'wb') as file:
        file.write(response.content)

    return path


def download_image(url, name, folder='images'):
    """Функция для скачивания картинок"""

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    path = f'{os.getcwd()}/{folder}/{name}'
    with open(path, 'wb') as file:
        file.write(response.content)

    return path


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError(response.history)


def parse_book_page(response):
    """Функция для получения информации о книге"""

    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.select_one('h1').text.split('::')

    genres = soup.select('.d_book > a')
    book_ganres = [genre.text for genre in genres]

    comments = soup.select('.texts .black')
    book_comments = [comment.text for comment in comments]

    image = soup.select_one('.bookimage a img')['src']
    image_url = urljoin(response.url, image)

    return {
        'title': title.strip(),
        'author': author.strip(),
        'ganres': book_ganres,
        'comments': book_comments,
        'image_url': image_url
    }


def main():
    logger = logging.getLogger('ParserLog')
    logging.basicConfig(filename='app.log', filemode='w')
    logging.info('This will get logged to a file')

    logger.setLevel(level=logging.INFO)
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    parser = argparse.ArgumentParser(description='Save books from tululu.org')
    parser.add_argument('start', help='Starting book', type=int, default=1)
    parser.add_argument('end', help='Ending book', type=int, default=10)
    args = parser.parse_args()

    start_id = args.start
    end_id = args.end

    for book_id in range(start_id, end_id + 1):
        text_url = 'https://tululu.org/txt.php'
        title_url = f'https://tululu.org/b{book_id}/'

        try:
            response = requests.get(title_url)
            response.raise_for_status()
            check_for_redirect(response)

            book_description = parse_book_page(response)
            image_name = urlsplit(
                book_description['image_url']
            ).path.split('/')[2]
            book_name = f"{book_id}. {book_description['title']}"

            download_txt(text_url, book_name)
            download_image(book_description['image_url'], image_name)
            print(textwrap.dedent(f'''
                    Заголовок: {book_description["title"]}
                    Автор: {book_description["author"]}
                    Жанры: {book_description["ganres"]}
                    Комменты: {book_description["comments"]}
                '''))
        except requests.HTTPError as error:
            print(f'HTTP request error: {error}. Use google.com to translate.')
            logger.info(f'HTTP request error: {error}. \
                Book {book_id} is not download!')
            continue
        except requests.ConnectionError:
            print('Connection error!')
            time.sleep(5)
            continue


if __name__ == "__main__":
    main()
