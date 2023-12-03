import os

from utils import TIME_FORMAT_TIME, File, JSONFile, Log, Time

README_PATH = 'README.md'

log = Log('update_readme')
DIR_DATA_VILLAGES = os.path.join('data', 'villages')


def main():
    time_str = TIME_FORMAT_TIME.stringify(Time.now())

    file_only_list = []
    n_dsds = 0
    n_gnds = 0
    n_villages = 0
    for file_only in os.listdir(DIR_DATA_VILLAGES):
        file_only_list.append(file_only)
        file_path = os.path.join(DIR_DATA_VILLAGES, file_only)

        data = JSONFile(file_path).read()
        n_dsds += 1
        n_gnds_for_dsd = len(data['children'])
        n_gnds += n_gnds_for_dsd
        for gnd in data['children']:
            n_villages_for_gnd = len(gnd['children'])
            n_villages += n_villages_for_gnd

    lines = [
        '# Villages of Sri Lanka',
        '',
        'Scrapes information about villages from http://moha.gov.lk:8090.',
        '',
        f'**{n_villages}** Villages from from **{n_gnds}**'
        + f' in **{n_dsds}** DSDs, scraped as of *{time_str}*.',
    ]

    for file_only in file_only_list:
        dsd_id = file_only.split('.')[0]
        lines.append(
            f'* [{dsd_id}]({os.path.join(DIR_DATA_VILLAGES, file_only)})'
        )

    File(README_PATH).write_lines(lines)
    log.info(f'Updated {README_PATH}')


if __name__ == '__main__':
    main()
