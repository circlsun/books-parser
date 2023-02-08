import os
import time
import json
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError(response.history)


def get_url(start_id, end_id):
    links = []

    for page in range(start_id, end_id):
        scifi_url = f'https://tululu.org/l55/{page}'
        response = requests.get(scifi_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        books_scifi = soup.select('.bookimage')

        for book_scifi in books_scifi:
            links.append(urljoin(
                response.url, book_scifi.select_one('a')['href']
                ))
    return links


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

    name = f'{sanitize_filename(filename)}'
    path = f'{os.getcwd()}/{folder}/{name}.txt'
    with open(path, 'wb') as file:
        file.write(response.content)

    return f'{folder}/{name}.txt'


def download_image(url, name, folder='images'):
    """Функция для скачивания картинок"""

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    path = f'{os.getcwd()}/{folder}/{name}'
    with open(path, 'wb') as file:
        file.write(response.content)

    return f'{folder}/{name}'


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
    parser = argparse.ArgumentParser(description='Save books from tululu.org')
    parser.add_argument(
        '--start_page', type=int, default=1,
        help='Starting book')
    parser.add_argument(
        '--end_page', type=int, default=701,
        help='Ending book')
    parser.add_argument(
        '--skip_imgs',  action='store_false', default=True,
        help='Argument for not to download the images')
    parser.add_argument(
        '--skip_txt',  action='store_false', default=True,
        help='Argument for not to download the text')
    parser.add_argument(
        '--json_path', default='books',
        help='Path for <.json> file')
    parser.add_argument(
        '--dest_folder', default='json',
        help='Path for text and images files')

    args = parser.parse_args()
    start_id = args.start_page
    end_id = args.end_page
    skip_images = args.skip_imgs
    skip_text = args.skip_txt
    books_folder = args.dest_folder
    json_folder = args.json_path

    os.makedirs(books_folder, exist_ok=True)
    os.makedirs(json_folder, exist_ok=True)

    text_url = 'https://tululu.org/txt.php'
    books_url = get_url(start_id, end_id)
    books_description = []
    for title_url in books_url:
        print(f'Download the book: {title_url}')
        book_id = title_url.split('/')[3][1:]
        book_description = {}
        try:
            response = requests.get(title_url)
            response.raise_for_status()
            check_for_redirect(response)

            book_description = parse_book_page(response)
            image_name = urlsplit(book_description['image_url'])\
                .path.split('/')[2]
            book_name = f"{book_id}. {book_description['title']}"

            if skip_text:
                text_path = download_txt(text_url, book_name, books_folder)
            else:
                text_path = None
            if skip_images:
                image_path = download_image(
                    book_description['image_url'], image_name, books_folder)
            else:
                image_path = None
            book_description = {
                    "title": book_description["title"],
                    "author": book_description["author"],
                    "img_src": image_path,
                    "book_path": text_path,
                    "comments": book_description["comments"],
                    "genres": book_description["ganres"]
            }

        except requests.HTTPError as error:
            print(f'HTTP request error: {error}. Use google.com to translate.')
            continue
        except requests.ConnectionError:
            print('Connection error!')
            time.sleep(5)
            continue

        books_description.append(book_description)
        book_json = json.dumps(books_description, ensure_ascii=False, indent=2)

        with open(
            f'{json_folder}/{"books_description.json"}', 'w', encoding='utf8'
        ) as my_file:
            my_file.write(book_json)


if __name__ == "__main__":
    main()
