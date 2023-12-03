import os
import random
import time

from utils import JSONFile, Log

from lk_villages import Region
from workflows.build_dsds import DSD_DATA_PATH

log = Log('pipeline')

MAX_COMPLETED_RUNS = 5
log.debug(f'🪛{MAX_COMPLETED_RUNS=}')
DIR_DATA_VILLAGES = os.path.join('data', 'villages')


def random_sleep():
    random_t = random.random() * 10 + 10
    log.debug(f"😴Sleeping for {random_t:.3f} seconds.")
    time.sleep(random_t)


if __name__ == '__main__':
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
