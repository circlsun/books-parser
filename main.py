import os
import argparse
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

    return os.path.join(folder, name)


def download_image(url, name, folder='images'):
    """Функция для скачивания картинок"""

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    path = f'{os.getcwd()}/{folder}/{name}'
    with open(path, 'wb') as file:
        file.write(response.content)

    return os.path.join(folder, name)


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.exceptions.HTTPError


def parse_book_page(response):
    """Функция для получения информации о книге"""

    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.find('h1').text.split('::')

    genres = soup.find('span', class_='d_book').find_all('a')
    book_ganres = [genre.text for genre in genres]

    comments = soup.find_all(class_='texts')
    book_comments = [comment.find(class_='black').text for comment in comments]

    image = 'images/nopic.gif'
    if response.url != 'https://tululu.org/':
        image = soup.find(class_='bookimage').find('a').find('img')['src']
    image_url = urljoin('https://tululu.org/', image)

    return {
        'title': title.strip(),
        'author': author.strip(),
        'ganres': book_ganres,
        'comments': book_comments,
        'image_url': image_url
    }


def main():
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
            book_info = parse_book_page(response)
            imagename = urlsplit(book_info['image_url']).path.split('/')[2]
            filename = f"{book_id}. {book_info['title']}"
            download_txt(text_url, filename)
            download_image(book_info['image_url'], imagename)
            print('Заголовок:', book_info['title'])
            print('Автор:', book_info['author'])
            print('Жанры:', book_info['ganres'])
            print('Комментарии:', book_info['comments'])
            print()
        except requests.exceptions.HTTPError:
            pass


if __name__ == "__main__":
    main()
