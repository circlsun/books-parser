import os
import requests


def save_book(url, path):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)
    check_for_redirect(response)
    return response.url


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.exceptions.HTTPError


os.makedirs('books', exist_ok=True)

id_start = 200
for i in range(id_start, id_start + 10):
    path = f'{os.getcwd()}/books/id{i}.txt'
    url = f'https://tululu.org/txt.php?id={i}'

    try:
        save_book(url, path)
    except requests.exceptions.HTTPError:
        os.remove(f'{os.getcwd()}/books/id{i}.txt')
