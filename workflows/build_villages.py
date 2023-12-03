import random
import time

from utils import JSONFile, Log

from lk_villages import Region
from workflows.build_dsds import DSD_DATA_PATH

log = Log('pipeline')

N_SAMPLES = 5
log.debug(f'{N_SAMPLES=}')


def random_sleep():
    random_t = random.random() * 1
    log.debug(f"😴Sleeping for {random_t:.3f} seconds.")
    time.sleep(random_t)


if __name__ == '__main__':
    data_list = JSONFile(DSD_DATA_PATH).read()
    random_data_list = random.sample(data_list, N_SAMPLES)

    for d in random_data_list:
        dsd = Region(**d)
        dsd.write()
        random_sleep()
