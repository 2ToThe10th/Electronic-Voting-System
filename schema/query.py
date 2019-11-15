import models


def create_user(id, user_name=''):
    return models.User.get_or_create(id=id, name=user_name)[0].id


def create_poll(owner_id, type_title, title='', desc=''):
    return models.Poll.get_or_create(owner_id=owner_id, type=type_title, title=title, description=desc)[0].id
