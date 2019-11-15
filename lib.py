import json
import schema.query as queries
from normalizer import normalize_config
from vote_functions import vote_data


def get_types():
    config = json.load(open('config.json'))
    return list(config.keys())


def creation(type):
    config = json.load(open('config.json'))
    questions = []
    for key in config[type]:
        add = ''
        if len(config[type][key]) == 2:
            add = config[type][key][1]
        questions.append([key, f'Provide your {key}' + add])
    return questions


def get_creator_answers(chat_id, type, answers):
    poll = json.load(open('config.json'))[type]
    for answer in answers:
        poll[answer[0]] = answer[1]
    if normalize_config[type](poll):
        poll_id = queries.create_poll(chat_id, type, poll)
        return poll_id
    return -1


def vote(id):
    owner, type, config = queries.get_poll_data(id)
    return type, vote_data[type](config)


def get_vote(user_id, poll_id, answer):
    queries.create_vote(user_id, poll_id, answer)
