def choose_one_vote(poll):
    return poll['question'], poll['variants']


vote_data = {
    'choose_one': choose_one_vote
}