import peewee
from peewee import CharField, Model, IntegerField, ForeignKeyField, BooleanField

from db.database import db


class Person(Model):
    username = CharField(null=True)
    name = CharField(null=True)
    is_recipient = BooleanField(default=False)
    karma_level = IntegerField(default=0)

    class Meta:
        table_name = 'Users'
        database = db


class RelationShip(Model):
    donor = ForeignKeyField(Person)
    recipient = ForeignKeyField(Person)

    class Meta:
        table_name = 'Relations'
        database = db


def create_tables():
    import os
    if not os.path.isfile('../'):
        db.connect()
        db.create_tables([Person, RelationShip])

