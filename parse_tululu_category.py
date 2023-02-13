import os
import time
import json
import textwrap
import argparse
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from parse_tululu_all import check_for_redirect, download_txt
from parse_tululu_all import download_image, parse_book_page


def get_urls(start_id, end_id):
    links = []

    for page in range(start_id, end_id):
        scifi_url = f'https://tululu.org/l55/{page}'
        response = requests.get(scifi_url)
        response.raise_for_status()
        check_for_redirect(response)

        soup = BeautifulSoup(response.text, 'lxml')
        books_scifi = soup.select('.bookimage')

        for book_scifi in books_scifi:
            links.append(urljoin(
                response.url, book_scifi.select_one('a')['href']
                ))
    return links


def main():
    parser = argparse.ArgumentParser(description='Save books from tululu.org')
    parser.add_argument(
        '--start_page', type=int, default=1,
        help='Starting book')
    parser.add_argument(
        '--end_page', type=int, default=5,
        help='Ending book')
    parser.add_argument(
        '--skip_imgs',  action='store_true',
        help='Argument for not to download the images')
    parser.add_argument(
        '--skip_txt',  action='store_true',
        help='Argument for not to download the text')
    parser.add_argument(
        '--json_path', default='json',
        help='Path for <.json> file')
    parser.add_argument(
        '--dest_folder', default='books',
        help='Path for text and images files')

    args = parser.parse_args()
    start_id = args.start_page
    end_id = args.end_page
    skip_images = args.skip_imgs
    skip_text = args.skip_txt
    books_folder = args.dest_folder
    json_folder = args.json_path
    print(skip_images, skip_text)

    os.makedirs(books_folder, exist_ok=True)
    os.makedirs(json_folder, exist_ok=True)

    text_url = 'https://tululu.org/txt.php'
    book_urls = get_urls(start_id, end_id)
    books_description = []
    for title_url in book_urls:
        print(f'Link of the book: {title_url}')
        book_id = title_url.split('/')[3][1:]
        try:
            response = requests.get(title_url)
            response.raise_for_status()
            check_for_redirect(response)

            book_description = parse_book_page(response)
            image_name = urlsplit(book_description['image_url'])\
                .path.split('/')[2]
            book_name = f"{book_id}. {book_description['title']}"

            if skip_text:
                text_path = None
            else:
                text_path = download_txt(text_url, book_name, books_folder)

            if skip_images:
                image_path = None
            else:
                image_path = download_image(
                    book_description['image_url'], image_name, books_folder)

            book_description = {
                    "title": book_description["title"],
                    "author": book_description["author"],
                    "img_src": image_path,
                    "book_path": text_path,
                    "comments": book_description["comments"],
                    "genres": book_description["ganres"]
            }

        except requests.HTTPError as error:
            print(textwrap.dedent(f'''
            The previous book is not available for download.
            HTTP error: {error}. Use google.com to translate.
            '''))
            continue
        except requests.ConnectionError:
            print('Connection error!')
            time.sleep(5)
            continue

        books_description.append(book_description)
        with open(
            f'{json_folder}/{"books_description.json"}', 'w', encoding='utf8'
        ) as jsnfile:
            json.dump(books_description, jsnfile, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
