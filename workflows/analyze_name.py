import re

from utils import Log, TSVFile

from workflows.build_villages import ALL_PATH

log = Log('analyze_name')


def clean_name(x: str) -> str:
    x = x.replace('-', ' ')
    x = re.sub(r'\s+', ' ', x)
    x = x.strip()
    return x.lower()


def get_names():
    data_list = TSVFile(ALL_PATH).read()
    names = []
    for d in data_list:
        names.append(clean_name(d['name']))
    return names


def get_xgrams(name: str) -> list[str]:
    return name.split(' ')
    # xgrams = []
    # for i in range(len(name) - 2):
    #     xgram = name[i: i + 3]
    #     xgrams.append(xgram)
    # return xgrams


def analyze():
    names = get_names()
    log.debug(f'Got {len(names)} names')
    xgram_to_n = {}
    for name in names:
        x_grams = get_xgrams(name)
        for x_gram in x_grams:
            xgram_to_n[x_gram] = xgram_to_n.get(x_gram, 0) + 1

    xgram_to_n = sorted(xgram_to_n.items(), key=lambda x: x[1], reverse=False)
    for xgram, n in xgram_to_n[-100:]:
        log.info(f'{xgram}\t{n}')
    return x_gram


if __name__ == '__main__':
    analyze()
