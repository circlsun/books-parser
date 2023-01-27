import os
import sys
import requests
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit
import argparse
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

    response = requests.get(url)
    response.raise_for_status()

    name = f"{sanitize_filename(filename)}"
    path = f'{os.getcwd()}/{folder}/{name}.txt'

    with open(path, 'wb') as file:
        file.write(response.content)

    check_for_redirect(response)
    return os.path.join(folder, name)


def download_image(url, name, folder='images'):
    """Функция для скачивания картинок"""
    response = requests.get(url)
    response.raise_for_status()

    path = f'{os.getcwd()}/{folder}/{name}'
    with open(path, 'wb') as file:
        file.write(response.content)

    return os.path.join(folder, name)


def get_filename(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_teg = soup.find('h1').text.split('::')

    if response.url != 'https://tululu.org/':
        img = soup.find(class_='bookimage').find('a').find('img')['src']
    else:
        img = 'images/nopic.gif'
    return title_teg[0].strip(), urljoin('https://tululu.org/', img)


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.exceptions.HTTPError


def parse_book_page(soup):

    teg = soup.find('h1').text.split('::')
    title = teg[0].strip()
    author = teg[1].strip()

    comments = soup.find_all(class_='texts')
    book_comments = [comment.find(class_='black').text for comment in comments]

    genres = soup.find('span', class_='d_book').find_all('a')
    book_ganre = [genre.text for genre in genres]

    book_info = {
        'title': title,
        'author': author,
        'ganre': book_ganre,
        'comments': book_comments,
    }
    return book_info


def main():
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    parser = argparse.ArgumentParser(description='Save books from tululu.org')
    parser.add_argument('start', help='Starting book', type=int, default=1)
    parser.add_argument('end', help='Ending book', type=int, default=10)
    args = parser.parse_args()

    start_id = args.start
    end_id = args.end

    for i in range(start_id, end_id + 1):
        url = f'https://tululu.org/txt.php?id={i}'
        url_title = f'https://tululu.org/b{i}/'

        response = requests.get(url_title)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        title, url_img = get_filename(response)
        imgname = urlsplit(url_img).path.split('/')[2]
        filename = f"{i}. {title}"

        try:
            download_txt(url, filename)
            download_image(url_img, imgname)
            print('Заголовок:', parse_book_page(soup)['title'])
            print('Автор:', parse_book_page(soup)['author'])
            print('Жанр:', parse_book_page(soup)['ganre'])
            print('Комментарии:', parse_book_page(soup)['comments'])
            print()
        except requests.exceptions.HTTPError:
            os.remove(f'{os.getcwd()}/books/{filename}.txt')


if __name__ == "__main__":
    main()
