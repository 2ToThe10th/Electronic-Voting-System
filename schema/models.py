from peewee import *

db = SqliteDatabase('evoting.db')


class User(Model):
    name = CharField(max_length=100, default='')
    id = IntegerField(primary_key=True)

    class Meta:
        database = db


class Poll(Model):
    title = CharField(max_length=100, default='Voting number ' + str(id))
    description = TextField(default='')
    type = CharField(max_length=100)

    owner_id = ForeignKeyField(User)

    class Meta:
        database = db


class Votes(Model):
    user_id = ForeignKeyField(User, backref='voter')
    voting_id = ForeignKeyField(Poll, backref='voting', index=True)
    answer_json = TextField()

    class Meta:
        database = db
        primary_key = CompositeKey('user_id', 'voting_id')


db.connect()
db.create_tables([User, Poll, Votes])
