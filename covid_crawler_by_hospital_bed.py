from abc import ABC
from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from common import Common
from covid_crawler_base import COVIDCrawlerBase


@dataclass
class BedCount:
    severe: int
    severe_total: int
    moderate: int
    moderate_total: int

    def _get_text(self, count: int, total: int) -> str:
        rate = (total - count) / total * 100
        return f'{rate:.1f}% ({total - count:,}/{total:,})'

    def __str__(self):
        return f'중환자 병상 가동률: {self._get_text(self.severe, self.severe_total)}\n' \
               f'일반 병상 가동률: {self._get_text(self.moderate, self.moderate_total)}'


class COVIDCrawlerByBed(COVIDCrawlerBase, ABC):
    SOURCE_URL: str = 'http://ncov.mohw.go.kr'

    @property
    def message(self):
        return f'COVID-19 병상 현황 업데이트 [*{self.when}*]\n\n{self.bed_status}'

    def __init__(self):
        req = requests.get(self.SOURCE_URL)
        soup = BeautifulSoup(req.text, 'html.parser')

        self.when = soup.select_one('.hospitalNum .title1 .livedate').text.strip().split(',')[0].replace('(', '').replace(')', '')
        self.bed_status = self._get_bed_status(soup)

    def _get_bed_status(self, soup: BeautifulSoup) -> Optional[BedCount]:
        table = soup.select_one('.hospitalStatus table')
        rows = table.select('tr')
        if len(rows) != 3:
            raise Exception('table row length not match!')
        severe_count, severe_total = self._get_bed_count_by_row(rows[1])
        moderate_count, moderate_total = self._get_bed_count_by_row(rows[2])
        return BedCount(severe_count, severe_total, moderate_count, moderate_total)

    def _get_bed_count_by_row(self, row: Tag) -> (int, int):
        cells = row.select('td')
        if len(cells) != 3:
            raise Exception('table cell length not match!')
        total = Common.to_number(cells[1].text)
        count = Common.to_number(cells[2].text)
        return count, total


if __name__ == '__main__':
    print(COVIDCrawlerByBed().message)
