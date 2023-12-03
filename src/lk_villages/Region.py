import json
import os
from dataclasses import dataclass
from functools import cached_property

from bs4 import BeautifulSoup
from gig import EntType
from utils import JSONFile, Log

from utils_future import WWW

log = Log('pipeline')

ENT_TYPE_TO_CHILD_ID_LEN = {
    'province': 1,
    'district': 2,
    'dsd': 3,
    'gnd': 2,
}

ENT_TYPE_TO_QUERY_ACTION = {
    'dsd': 'ds',
    'gnd': 'gn_div',
}


@dataclass
class Region:
    id: str
    name: str
    query_id: str

    @staticmethod
    def provinces() -> list['Region']:
        return [
            Region("LK-1", "Western Province", "63"),
            Region("LK-2", "Central Province", "64"),
            Region("LK-3", "Southern Province", "65"),
            Region("LK-4", "Northern Province", "66"),
            Region("LK-5", "Eastern Province", "67"),
            Region("LK-6", "North Western Province", "68"),
            Region("LK-7", "North Central Province", "69"),
            Region("LK-8", "Uva Province", "70"),
            Region("LK-9", "Sabaragamuwa Province", "71"),
        ]

    @cached_property
    def ent_type(self) -> EntType:
        return EntType.from_id(self.id)

    @cached_property
    def query_action(self) -> str:
        return ENT_TYPE_TO_QUERY_ACTION.get(
            self.ent_type.name, self.ent_type.name
        )

    @cached_property
    def children(self) -> list['Region']:
        url = 'http://moha.gov.lk:8090/lifecode/views/fetch.php'
        child_id_len = ENT_TYPE_TO_CHILD_ID_LEN.get(self.ent_type.name, None)
        if not child_id_len:
            return []

        content = WWW(url).post(
            dict(action=self.query_action, query=self.query_id)
        )
        data = json.loads(content)
        html = data['output']
        soup = BeautifulSoup(html, 'html.parser')
        child_regions = []
        for option in soup.find_all('option'):
            text = option.text
            if ': ' not in text:
                continue
            child_query_id = option['value']
            DELIM = ': '
            tokens = text.split(DELIM)
            child_id_prefix, child_name = tokens[0], DELIM.join(tokens[1:])
            child_id_prefix = child_id_prefix.rjust(child_id_len, '0')
            child_id = self.id + child_id_prefix
            child = Region(child_id, child_name, child_query_id)

            child_regions.append(child)
        n_expected = int(data['count'])
        n_actual = len(child_regions)
        assert n_expected == n_actual, f'{n_expected} != {n_actual}'
        log.debug(f'Fetched {n_actual} child regions for {self.id}')
        return child_regions

    @cached_property
    def data_shallow(self) -> dict:
        return dict(
            id=self.id,
            name=self.name,
            query_id=self.query_id,
        )

    @cached_property
    def data(self) -> dict:
        data = self.data_shallow
        children = [child.data for child in self.children]
        if children:
            data['children'] = children
        return data

    @cached_property
    def data_path(self) -> str:
        return os.path.join('data', 'villages', f'{self.id}.json')

    def write(self):
        if os.path.exists(self.data_path):
            log.warning(f'Data already exists at {self.data_path}.')
            return False
        JSONFile(self.data_path).write(self.data)
        log.info(f'Wrote {self.data_path}')
        return True
