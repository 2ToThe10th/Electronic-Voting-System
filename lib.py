import json
import schema.query as queries
from normalizer import normalize_config


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
        queries.create_poll(chat_id, type, poll)
        print(poll)
        return True
    return False




# def choose_one_creation(id, question, variants):
#     config = json.load(open('config.json'))
#     config['question'] = question
#     config['variants'] = variants
#     # push_to_database
#
# def choose_one_vote_before(config):
#     # push_to_database:  id_user id_poll number
#     return config['say'], config['variants'], confi
#
#
# # dict: type - vote process functions
# vote_functions_before = {
#     'choose_one': choose_one_vote_before
# }
#
# def vote_before(id):
#     # get type, config from database
#     ans = vote_functions_before[type](config)
#
#print(creation(get_types()[0]))
#print(get_creator_answers(get_types()[0], [['question', 'my question'], ['variants', 'Provide your variants, list with a comma']]))
