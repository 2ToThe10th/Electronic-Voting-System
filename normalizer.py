def choose_one_normalizer(poll):
    try:
        poll['variants'] = poll['variants'].strip().split(',')
        return True
    except Exception:
        return False


def choose_many_normalizer(poll):
    try:
        poll['variants'] = poll['variants'].strip().split(',')
        return True
    except Exception:
        return False


def choose_prioritets_normalizer(poll):
    try:
        poll['variants'] = poll['variants'].strip().split(',')
        poll['power'] = int(poll['power'])
        return True
    except Exception:
        return False


def choose_by_prioritets_normalizer(poll):
    try:
        poll['variants'] = poll['variants'].strip().split(',')
        return True
    except Exception:
        return False



normalize_config = {
    'choose_one': choose_one_normalizer,
    'choose_many': choose_many_normalizer,
    'choose_prioritets': choose_prioritets_normalizer,
    'choose_by_prioritets': choose_by_prioritets_normalizer,
}