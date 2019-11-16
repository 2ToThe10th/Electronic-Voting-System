from . import models


def create_user(id, user_name=''):
    user_bool = models.User.get_or_create(id=id, name=user_name)
    id = user_bool[0].id
    if user_bool[1]:
        print('User created with id =', id)
    else:
        print('User with id =', id, 'already exists')
    return id


def create_poll(owner_id, type_title, config, title='', desc=''):
    poll_bool = models.Poll.get_or_create(owner=models.User.get_by_id(owner_id), type=type_title,
                                          config_json=config, title=title, description=desc)
    id = poll_bool[0].id
    if poll_bool[1]:
        print('Poll created with id =', id)
    else:
        print('Poll with id =', id, 'already exists')
    return id


def get_poll_data(poll_id):
    poll = models.Poll.get_by_id(poll_id)
    return poll.owner_id, poll.type, poll.config_json


def create_vote(user_id, poll_id, answer_json):
    user = models.User.get_by_id(user_id)
    poll = models.Poll.get_by_id(poll_id)
    try:
        vote_bool = models.Votes.get_or_create(user=user, poll=poll, answer_json=answer_json)[1]
    except models.IntegrityError:
        vote_bool = False

    if vote_bool:
        print('Vote created with user_id, poll_id =', str(user_id) + ',', poll_id)
    else:
        print('Vote with user_id, poll_id =', str(user_id) + ',', poll_id, 'already exists')
    return user_id, poll_id


def get_vote_data(user_id, poll_id):
    vote = models.Votes.get_by_id((user_id, poll_id))
    return vote.user_id, vote.poll_id, vote.answer_json


def get_votes_by_poll(poll_id):
    poll = models.Poll.get_by_id(poll_id)
    votes = models.Votes.select().where(models.Votes.poll == poll)
    return list(map(lambda x: x.__dict__['__data__'], votes)), poll.config_json, poll.type


def is_owner(poll_id, user_id):
    poll = models.Poll.get_by_id(poll_id)
    return poll.owner_id == user_id


def create_stockholder(user_id, poll_id, weight):
    user = models.User.get_by_id(user_id)
    poll = models.Poll.get_by_id(poll_id)
    try:
        stock_bool = models.StockHolder.get_or_create(user=user, poll=poll, weight=weight)[1]
    except models.IntegrityError:
        stock_bool = False

    if stock_bool:
        print('Stockholder was created with user_id, poll_id =', str(user_id) + ',', poll_id)
    else:
        print('Stockholder with user_id, poll_id =', str(user_id) + ',', poll_id, 'already exists')
    return user_id, poll_id


def create_access(user_id, poll_id):
    user = models.User.get_by_id(user_id)
    poll = models.Poll.get_by_id(poll_id)
    try:
        access_bool = models.AccessPoll.get_or_create(user=user, poll=poll)[1]
    except models.IntegrityError:
        access_bool = False

    if access_bool:
        print('Access for user_id =', user_id, 'was created for poll_id =', poll_id)
    else:
        print('Access for user_id =', user_id, 'already exists for poll_id =', poll_id)
    return user_id, poll_id


def has_user_voted(user_id, poll_id):
    elements = models.Votes.select().where(models.Votes.poll_id == poll_id, models.Votes.user_id == user_id)
    return len(elements) != 0


def has_user_access(user_id, poll_id):
    try:
        models.User.get_by_id(user_id)
        models.Poll.get_by_id(poll_id)
    except:
        return False

    users_with_access = models.AccessPoll.select().where(models.AccessPoll.poll_id == poll_id)
    return len(users_with_access) == 0 or user_id in map(lambda el: el.user_id, users_with_access)
