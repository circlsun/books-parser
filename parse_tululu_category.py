import os
import time
import textwrap
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError(response.history)


def get_url():
    links = []

    for page in range(1, 5):
        scifi_url = f'https://tululu.org/l55/{page}'
        response = requests.get(scifi_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        books_scifi = soup.find_all(class_='bookimage')

        for book_scifi in books_scifi:
            links.append(urljoin(response.url, book_scifi.find('a')['href']))
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


def parse_book_page(response):
    """Функция для получения информации о книге"""

    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.find('h1').text.split('::')

    genres = soup.find('span', class_='d_book').find_all('a')
    book_ganres = [genre.text for genre in genres]

    comments = soup.find_all(class_='texts')
    book_comments = [comment.find(class_='black').text for comment in comments]

    image = soup.find(class_='bookimage').find('a').find('img')['src']
    image_url = urljoin(response.url, image)

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

    text_url = 'https://tululu.org/txt.php'
    books_url = get_url()

    for title_url in books_url:

        book_id = title_url.strip('/')[3]

        try:
            response = requests.get(title_url)
            response.raise_for_status()
            check_for_redirect(response)

            book_description = parse_book_page(response)
            image_name = urlsplit(book_description['image_url']).path.split('/')[2]
            book_name = f"{book_id}. {book_description['title']}"
            print(book_name)
            download_txt(text_url, book_name)
            download_image(book_description['image_url'], image_name)
            print(textwrap.dedent(f'''
                    Заголовок: {book_description["title"]}
                    Автор: {book_description["author"]}
                    Жанры: {book_description["ganres"]}
                '''))
        except requests.HTTPError as error:
            print(f'HTTP request error: {error}. Use google.com to translate.')
            continue
        except requests.ConnectionError:
            print('Connection error!')
            time.sleep(5)
            continue


if __name__ == "__main__":
    main()
