import os
import random
import time

from utils import JSONFile, Log, TSVFile

from lk_villages import Region
from workflows.build_dsds import DSD_DATA_PATH

log = Log('pipeline')

MAX_COMPLETED_RUNS = 1
log.debug(f'🪛{MAX_COMPLETED_RUNS=}')
DIR_DATA_VILLAGES = os.path.join('data', 'villages')
ALL_PATH = os.path.join('data', 'villages.tsv')


def random_sleep():
    random_t = random.random() * 5 + 5
    log.debug(f"😴Sleeping for {random_t:.3f} seconds.")
    time.sleep(random_t)


def scrape():
    if not os.path.exists(DIR_DATA_VILLAGES):
        os.mkdir(DIR_DATA_VILLAGES)

    data_list = JSONFile(DSD_DATA_PATH).read()

    n_completed_runs = 0
    for d in data_list:
        dsd = Region(**d)
        if dsd.write():
            random_sleep()
            n_completed_runs += 1
            if n_completed_runs >= MAX_COMPLETED_RUNS:
                break


def aggregate():
    data_list = []
    for file_only in os.listdir(DIR_DATA_VILLAGES):
        d = JSONFile(os.path.join(DIR_DATA_VILLAGES, file_only)).read()
        for gnd in d['children']:
            for village in gnd.get('children', []):
                data = dict(
                    village_id=village['id'],
                    name=village['name'],
                )
            data_list.append(data)
    data_list = sorted(data_list, key=lambda d: d['village_id'])
    TSVFile(ALL_PATH).write(data_list)
    log.debug(f'Wrote {len(data_list)} villages to {ALL_PATH}')


if __name__ == '__main__':
    scrape()
    aggregate()
