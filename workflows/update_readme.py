import os

from gig import Ent
from utils import TIME_FORMAT_TIME, File, JSONFile, Log, Time

from workflows.build_villages import DIR_DATA_VILLAGES

README_PATH = 'README.md'

log = Log('update_readme')


def main():
    time_str = TIME_FORMAT_TIME.stringify(Time.now())

    file_only_list = []
    n_dsds = 0
    n_gnds = 0
    n_villages = 0
    n_file_size = 0
    for file_only in os.listdir(DIR_DATA_VILLAGES):
        file_only_list.append(file_only)
        file_path = os.path.join(DIR_DATA_VILLAGES, file_only)
        file_size = os.path.getsize(file_path)
        n_file_size += file_size
        data = JSONFile(file_path).read()
        n_dsds += 1
        n_gnds_for_dsd = len(data['children'])
        n_gnds += n_gnds_for_dsd
        for gnd in data['children']:
            n_villages_for_gnd = len(gnd.get('children', []))
            n_villages += n_villages_for_gnd

    n_file_size_m = n_file_size / 1_000_000
    lines = [
        '# Villages of Sri Lanka',
        '',
        'Scrapes information about villages from http://moha.gov.lk:8090.',
        '',
        f'**{n_villages:,}** Villages from **{n_gnds:,}** GNDs'
        + f' in **{n_dsds:,}** DSDs ({n_file_size_m:.3f}MB), scraped as of *{time_str}*.',
    ]

    previous_province_id = None
    for file_only in sorted(file_only_list):
        dsd_id = file_only.split('.')[0]
        province_id = dsd_id[:4]
        try:
            dsd = Ent.from_id(dsd_id)
            dsd_name = dsd.name
        except BaseException:
            dsd_name = '❔'
        if province_id != previous_province_id:
            previous_province_id = province_id
            province = Ent.from_id(province_id)
            lines.append('')
            lines.append(f'## {province_id} - {province.name}')
            lines.append('')
        lines.append(
            f'* [{dsd_id}]({os.path.join(DIR_DATA_VILLAGES, file_only)}) - {dsd_name}'
        )

    File(README_PATH).write_lines(lines)
    log.info(f'Updated {README_PATH}')


if __name__ == '__main__':
    main()
