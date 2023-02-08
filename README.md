# Parser of books from tululu.org

App for parsing info and downloading books and their covers from of [Tululu](https://tululu.org/).

### How to install

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Usage main.py

Just run the python script `main.py` with the following concole command:
```
python main.py 30 40
```
Where argument <30> is the starting book, and <40> is the last book to download.

#### For example:
```
python main.py 50 53
```
Books from <50> to <53> will be downloaded to the 'books' folder and their covers to the 'images' folder.
And in console the result will be: 
```
Заголовок: Этика перераспределения
Автор: Жувенель Бертран     
Жанр: ['Деловая литература']
Комментарии: []

Заголовок: Как это делается - Финансовые, социальные и информационные технологии
Автор: Автор неизвестен     
Жанр: ['Деловая литература']
Комментарии: []

Заголовок: Как найти высокооплачиваемую работу с помощью Internet
Автор: Рудинштейн Марк
Жанр: ['Деловая литература', 'Прочая компьютерная литература']
Комментарии: ['Набор общеизвестных фраз и ничего личного, привнесенного автором. Скучно, малоинформативно, не стоит тратить время на книгу тем, кто собирается таким образом искать работу через Интернет.']
```
### Usage parse_tululu_category.py

Just run the python script `parse_tululu_category.py` with the following concole command:
```
python parse_tululu_category.py
```
Only the first five pages will be downloaded to the default folder `books` And the `book_description' file.json` to the default folder `json'.(about 100 books).

#### For example:
```
python main.py 50 53
```
Books from <50> to <53> will be downloaded to the 'books' folder and their covers to the 'images' folder.
And in console the result will be: 
```

```

### Project Goals

The code is written for educational purposes for the online-course of the Python Web developer on [Devmen](https://dvmn.org/)