"""
Реалізуйте скрипт для пошуку цитат за тегом, за ім'ям автора або набором тегів.
Скрипт виконується в нескінченному циклі і за допомогою звичайного оператора input
приймає команди у наступному форматі команда: значення.
Приклад:
name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin;
tag:life — знайти та повернути список цитат для тега life;
tags:life,live — знайти та повернути список цитат,
    де є теги life або live (примітка: без пробілів між тегами life, live);
exit — завершити виконання скрипту;

Виведення результатів пошуку лише у форматі utf-8;

Додаткове завдання
Подумайте та реалізуйте для команд name:Steve Martin та tag:life
можливість скороченого запису значень для пошуку, як name:st та tag:li відповідно;

Виконайте кешування результату виконання команд name: та tag: за допомогою Redis,
щоб при повторному запиті результат пошуку брався не з MongoDB бази даних, а з кешу;
"""

from mongoengine import Q

from cache import cache
import connect
from models import Authors, Quotes


@cache
def get_authors():
    authors = Authors.objects()
    res = []
    for author in authors:
        res.append(f"name: {author.fullname} born_date: {author.born_date} born_location: {author.born_location}")
    return res


@cache
def get_one_author(fullname):
    quotes = Authors.objects(Q(fullname__startswith=fullname.capitalize()))
    res = []
    for quote in quotes:
        request = Quotes.objects (Q(author=quote.id))
        for item in request:
            res.append(f"{item.author.fullname}'s quote:{item.quote} tags: {item.tags}")
    return res


@cache
def get_quotes_tags():
    quotes = Quotes.objects()
    all_tags =[]
    for quote in quotes:
        tags = [tag for tag in quote.tags]
        all_tags.extend(tags)
    return all_tags


@cache
def get_some_quote_with_reg(tags):
    res =[]
    for tag in tags:
        quotes = Quotes.objects(Q(tags__startswith=tag))
        for quote in quotes:
            res.append(f"{quote.author.fullname} said about this topic ('{quote.tags}'): {quote.quote}")
    return res


def main():
    while True:
        commands = (input("---> Enter please command (like - name:name or tag:tag) ...    ")).split(":")
        if len(commands) == 1:
            if commands[0] == "exit":
                break
            elif commands[0] == "name":
                print(f"---> Choose author and try again")
                [print(res) for res in get_authors()]

            elif commands[0] == "tag":
                print(f"---> Choose at least one tag")
                [print(res) for res in get_quotes_tags()]

        elif commands[0] == "tag":
            tags = commands[1].split(",")
            [print(res) for res in get_some_quote_with_reg(tags)]

        elif commands[0] == "name":
            [print(res) for res in get_one_author(commands[1])]

        else:
            print("Try again")


if __name__ == '__main__':
    main()

