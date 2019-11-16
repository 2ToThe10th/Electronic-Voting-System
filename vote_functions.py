def choose_one_vote(poll):
    return poll['question'], poll['variants']


def choose_many_vote(poll):
    return poll['question'], poll['variants']


def choose_many_prioritets(poll):
    return poll['question'], poll['variants']


vote_data = {
    'choose_one': choose_one_vote,
    'choose_many': choose_many_vote,
    'choose_prioritets': choose_many_prioritets
}