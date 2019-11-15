import models


def create_type(title, config_json):
    return models.VotingType.create(config_json=config_json, title=title)


def create_user(user_name):
    return models.User.create(name=user_name)


def create_voting(voting_type, title='', desc=''):
    return models.Voting.create(voting_type=voting_type, title=title, description=desc)


def create_owner(user_id, voting_id):
    return models.Owner.create(user_id=user_id, voting_id=voting_id)


def get_config(type_id):
    return models.Type.get_by_id(type_id).config_json
