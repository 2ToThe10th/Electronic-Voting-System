def choose_one_vote(poll):
    return poll['question'], poll['variants']


def choose_many_vote(poll):
    return poll['question'], poll['variants']


def choose_prioritets(poll):
    return poll['question'], poll['variants'], poll['power']


def choose_by_prioritets(poll):
    return poll['question'], poll['variants']


def laws(poll):
    return poll['question']


vote_data = {
    'choose_one': choose_one_vote,
    'choose_many': choose_many_vote,
    'choose_prioritets': choose_prioritets,
    'choose_by_prioritets': choose_by_prioritets,
    'laws': laws,
}
