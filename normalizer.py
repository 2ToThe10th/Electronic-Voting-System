def choose_one_normalizer(poll):
    try:
        poll['variants'] = poll['variants'].strip().split(',')
        return True
    except Exception:
        return False


normalize_config = {
    'choose_one': choose_one_normalizer
}