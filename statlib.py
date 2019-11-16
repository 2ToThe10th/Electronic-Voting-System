import matplotlib.pyplot as plt
from schema import query
import json


def stats_choose_one(data, config, id):
    data = [int(i['answer_json']) for i in data]
    n = len(config['variants'])
    plt.hist(data, range=(1, n), bins=n)
    plt.xticks(list(range(1, n + 1)), config['variants'])
    plt.savefig('hists/hist' + str(id))
    plt.close()


def stats_choose_many(data, config, id):
    data2 =[]
    for i in data:
        print(i)
        i['answer_json'] = list(map(int, json.loads(i['answer_json'])))
        data2.extend(i['answer_json'])
    n = len(config['variants'])
    if len(data2):
        plt.hist(data2, range=(1, n+1), bins=n, rwidth=0.2)
        dd = {}
        for i in data2:
            if i not in dd:
                dd[i] = 1
            else:
                dd[i] += 1

        plt.xticks([0.5 + i for i in range(1, n + 1)], config['variants'])
        print(dd)
        plt.yticks(list(range(0, max(dd.values()) + 2)))
        plt.savefig('hists/hist' + str(id))
        plt.close()
        return True
    else:
        return False


custom_stats = {
    'choose_one': stats_choose_one,
    'choose_many': stats_choose_many,
}


def stats(id):
    data, config, type = query.get_votes_by_poll(id)
    print(data, config, type)

    custom_stats[type](data, json.loads(config), id)
