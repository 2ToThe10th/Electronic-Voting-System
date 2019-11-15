from peewee import *

db = SqliteDatabase('evoting.db')


class User(Model):
    name = CharField(max_length=100, default='')

    class Meta:
        database = db


class VotingType(Model):
    title = CharField(max_length=100, primary_key=True)
    config_json = TextField()

    class Meta:
        database = db


class Voting(Model):
    title = CharField(max_length=100, default='Voting number ' + str(id))
    description = TextField(default='')
    voting_type = ForeignKeyField(VotingType, backref='type title')
    owner_id = ForeignKeyField(User)

    class Meta:
        database = db


class Votes(Model):
    user_id = ForeignKeyField(User, backref='voter')
    voting_id = ForeignKeyField(Voting, backref='voting', index=True)
    answer_json = TextField()

    class Meta:
        database = db
        primary_key = CompositeKey('user_id', 'voting_id')


db.connect()
db.create_tables([User, VotingType, Voting, Votes])
