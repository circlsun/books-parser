import os
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
   
    response = requests.get(url)
    response.raise_for_status()

    name = f"{sanitize_filename(filename)}"
    path = f'{os.getcwd()}/{folder}/{name}.txt'
    with open(path, 'wb') as file:
        file.write(response.content)

    check_for_redirect(response)
    return os.path.join(folder, name)


def get_filename(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_teg = soup.find('h1').text.split('::')
    title = title_teg[0].strip()
    return title


# def save_book(url, path):
#     response = requests.get(url, allow_redirects=True)
#     response.raise_for_status()
#     with open(path, 'wb') as file:
#         file.write(response.content)
#     check_for_redirect(response)
#     return response.url


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.exceptions.HTTPError


def main():
    os.makedirs('books', exist_ok=True)
    id_start = 200
    for i in range(id_start, id_start + 10):
        url1 = f'https://tululu.org/txt.php?id={i}'
        url2 = 'https://tululu.org/b{i}/'
        filename = get_filename(url2)
        try:
            
            download_txt(url1, filename, folder='books')
        except requests.exceptions.HTTPError:
            os.remove(f'{os.getcwd()}/books/id{i}.txt')

if __name__=="__main__":
    main()
