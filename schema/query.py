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
    poll_bool = models.Poll.get_or_create(owner_id=models.User.get_by_id(owner_id), type=type_title,
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
