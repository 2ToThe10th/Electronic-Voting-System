import matplotlib.pyplot as plt
from schema import query
import json


def stats_choose_one(data, config, id):
    data = list(map(int, data[0]['answer_json']))
    n = len(config['variants'])
    plt.hist(data, range=(1, n), bins=n)
    plt.xticks(list(range(1, n + 1)), config['variants'])
    plt.savefig('hists/hist' + str(id))
    plt.close()



custom_stats = {
    'choose_one': stats_choose_one,
}


def stats(id):
    data, config, type = query.get_votes_by_poll(id)
    print(data, config, type)

    custom_stats[type](data, json.loads(config), id)
