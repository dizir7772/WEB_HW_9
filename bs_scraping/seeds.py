import json

import connect
from models import Authors, Quotes


def authors_seeds():
    with open("authors.json", "r", encoding="utf-8") as f:
        for jsonObj in json.load(f):
            authors_dict = jsonObj
            author = Authors(fullname=authors_dict.get("fullname"), born_date=authors_dict.get("born_date"),
                             born_location=authors_dict.get("born_location"),description=authors_dict.get("description"))
            author.save()


def quotes_seeds():
    with open("quotes.json", "r", encoding="utf-8") as f:
        for jsonObj in json.load(f):
            quotes_dict = jsonObj
            author = Authors.objects(fullname=quotes_dict.get("author"))
            author_id = [i.id for i in author]
            quote = Quotes(tags=quotes_dict.get("tags"), quote=quotes_dict.get("quote"), author=author_id[0])
            quote.save()


if __name__ == '__main__':
    authors_seeds()
    quotes_seeds()
