import requests
from bs4 import BeautifulSoup


url = 'https://tululu.org/b239/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

# title_tag = soup.find('main').find('header').find('h1')
# title_text = title_tag.text

img = soup.find('img', class_='bookimage')['src']

# text = soup.find('p', class_='entry-content')

# print(title_text)
print(img)
# print(text)
