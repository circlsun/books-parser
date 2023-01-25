import os
import requests


i = 32169
url = f'https://tululu.org/txt.php?id={i}'


def save_book(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


filename = f'id{i}'
os.makedirs('books', exist_ok=True)
path = f'{os.getcwd()}/books/{filename}'


for i in range(32169, 32179):
    save_book(url, path)
