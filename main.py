import os
import requests
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit
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


def get_filename(url):
    response = requests.get(url)
    response.raise_for_status()

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


def main():
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    id_start = 300
    for i in range(id_start, id_start + 10):
        url = f'https://tululu.org/txt.php?id={i}'
        url_title = f'https://tululu.org/b{i}/'

        title, img_url = get_filename(url_title)
        imgname = urlsplit(img_url).path.split('/')[2]
        filename = f"{i}. {title}"

        try:
            download_txt(url, filename)
            download_image(img_url, imgname)
        except requests.exceptions.HTTPError:
            os.remove(f'{os.getcwd()}/books/{filename}.txt')


if __name__ == "__main__":
    main()
