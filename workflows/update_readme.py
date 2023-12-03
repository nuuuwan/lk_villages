import os

from utils import TIME_FORMAT_TIME, File, Log, Time

README_PATH = 'README.md'

log = Log('update_readme')
DIR_DATA_VILLAGES = os.path.join('data', 'villages')


def main():
    time_str = TIME_FORMAT_TIME.stringify(Time.now())

    file_only_list = []
    for file_only in os.listdir(DIR_DATA_VILLAGES):
        file_only_list.append(file_only)
    n_villages = len(file_only_list)

    lines = [
        '# Villages of Sri Lanka',
        '',
        'Scrapes information about villages from http://moha.gov.lk:8090.',
        '',
        f'Villages for **{n_villages}** DSDs, scraped as of *{time_str}*.',
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
