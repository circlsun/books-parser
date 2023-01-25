import requests
from bs4 import BeautifulSoup


url = 'https://tululu.org/b239/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

title_teg = soup.find('h1').text.split('::')
title = title_teg[0].strip()
author = title_teg[1].strip()
img = soup.find(class_='bookimage').find('a').find('img')['src']

print('Автор:', author)
print('Заголовок:', title)
print('Обложка:', img)
