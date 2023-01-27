import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


url = 'https://tululu.org/b5/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

title_teg = soup.find('h1').text.split('::')
title = title_teg[0].strip()
author = title_teg[1].strip()
comments = soup.find_all(class_='texts')
book_comments = [comment.find(class_='black').text for comment in comments]


genres = soup.find('span', class_='d_book').find_all('a')
book_ganre = [genre.text for genre in genres]

img = soup.find(class_='bookimage').find('a').find('img')['src']
url_img = urljoin('https://tululu.org/', img)

print('Автор:', author)
print('Заголовок:', title)
print('Обложка:', url_img)
print('Жанр:', book_ganre)
print('Комментарии:', book_comments)
