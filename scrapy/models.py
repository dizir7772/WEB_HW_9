from mongoengine import Document, CASCADE
from mongoengine.fields import ListField, StringField, ReferenceField


class Authors(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    quote = StringField()
    author = ReferenceField(Authors, dbref=False, reverse_delete_rule=CASCADE)
    meta = dict(allow_inheritance=True)
