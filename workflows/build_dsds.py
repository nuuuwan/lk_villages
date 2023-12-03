import os

from utils import JSONFile, Log

from lk_villages import Region

DSD_DATA_PATH = os.path.join('data', 'dsds.json')
log = Log('build_dsd')


def main():
    if not os.path.exists('data'):
        os.mkdir('data')

    if os.path.exists(DSD_DATA_PATH):
        log.warning(
            f'DSD data already exists at {DSD_DATA_PATH}. Not building.'
        )
        return

    provinces = Region.provinces()
    data_list = []
    for province in provinces:
        districts = province.children
        for district in districts:
            dsds = district.children
            for dsd in dsds:
                data_list.append(dsd.data_shallow)

    JSONFile(DSD_DATA_PATH).write(data_list)
    log.debug(f'Wrote {len(data_list)} dsd to {DSD_DATA_PATH}')


if __name__ == '__main__':
    main()
