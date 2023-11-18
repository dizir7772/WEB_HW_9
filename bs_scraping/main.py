import json
from typing import List

import requests
from bs4 import BeautifulSoup


START_URL = 'http://quotes.toscrape.com'
urls = [START_URL]


def get_urls(url) -> List[str]:
    response = requests.get(urls[-1])
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        sub_link = soup.find('li', attrs={'class': 'next'}).find('a')['href']
        next_link = START_URL + sub_link
        urls.append(next_link)
        if sub_link:
            get_urls(next_link)
    except AttributeError:
        pass
    return urls


def parse_data(urls: List[str]):
    quotes = []
    authors = []
    for url in urls:
        html_doc = requests.get(url)

        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            body = soup.find_all('div', attrs={'class': 'quote'})

            for item in body:
                quote = item.find('span', attrs={'class': 'text'}).text.strip()  # ['text']
                tags = item.find('meta')['content'].strip()  # .extract()
                author = item.find('small', attrs={'class': 'author'}).text.strip()  # ['author']

                search_value = author
                found = False
                for dictionary in quotes:
                    if search_value in dictionary.values():
                        found = True
                        break
                if found:
                    pass
                else:
                    author_link = START_URL + item.find('a')['href']
                    author_doc = requests.get(author_link)
                    if author_doc.status_code == 200:
                        author_soup = BeautifulSoup(author_doc.content, 'html.parser')
                        born_date = author_soup.find('span', attrs={'class': 'author-born-date'}).text.strip()
                        born_location = author_soup.find('span', attrs={'class': 'author-born-location'}).text.strip()
                        description = author_soup.find('div', attrs={'class': 'author-description'}).text.strip()

                        authors.append({
                            'fullname': author,
                            'born_date': born_date,
                            'born_location': born_location,
                            'description': description,
                        })

                quotes.append({
                    'quote': quote,
                    'tags': tags.split(","),
                    'author': author
                })


    with open('quotes.json', 'w', encoding='utf-8') as fd:
        json.dump(quotes, fd, ensure_ascii=False)
    with open('authors.json', 'w', encoding='utf-8') as fd:
        json.dump(authors, fd, ensure_ascii=False)




if __name__ == '__main__':
    get_urls(START_URL)
    parse_data(urls)
