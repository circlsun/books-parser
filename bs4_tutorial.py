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
for comment in comments:
    print('Комменты:', comment.select('span'))

img = soup.find(class_='bookimage').find('a').find('img')['src']
url_img = urljoin('https://tululu.org/', img)

print('Автор:', author)
print('Заголовок:', title)
print('Обложка:', url_img)
