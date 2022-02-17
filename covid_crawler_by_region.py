import re
from abc import ABC
from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup

from common import Common
from covid_crawler_base import COVIDCrawlerBase


@dataclass
class DailyCount:
    region: str
    overall: int
    korea: int
    overseas: int
    rates_per_100k: float

    def to_message(self):
        if self.region == '합계':
            return f'*{self.region}*: *{self.overall:,}* (국내 {self.korea:,}, 해외유입 {self.overseas:,}, 10만명당 발생률 {self.rates_per_100k:.4f}%)'
        if self.region == '검역':
            return f'{self.region}: {self.overall} (국내 {self.korea:,}, 해외유입 {self.overseas:,})'
        return f'{self.region}: {self.overall} (국내 {self.korea:,}, 해외유입 {self.overseas:,}, 발생률 {self.rates_per_100k:.4f}%)'


@dataclass
class MapItem:
    title: str
    count: int

    def to_message(self):
        return f'{self.title}: {self.count:,}'


class COVIDCrawlerByRegion(COVIDCrawlerBase, ABC):
    SOURCE_URL: str = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13'

    @property
    def message(self):
        counts_available = list(filter(lambda count: count.overall > 0, self.counts))
        region_counts = list(map(lambda count: count.to_message(), counts_available))
        severe = f'오늘의 대한민국 COVID-19 [*{self.when}*]\n\n'

        if self.severe is not None:
            severe += f'*재원 위중증: {self.severe:,}*\n'
        if self.admitted is not None:
            severe += f'*신규입원: {self.admitted:,}*'

        message = '\n'.join(region_counts)
        return f'{severe}\n\n{message}'

    def __init__(self):
        req = requests.get(self.SOURCE_URL)
        soup = BeautifulSoup(req.text, 'html.parser')

        self.when = soup.find('p', {'class': 'info'}).text.strip()

        self._find_counts_by_region(soup)
        self._find_severes(soup)

    def _find_counts_by_region(self, soup):
        container = soup.find('div', {'class': 'mgt24'})
        rows = container.find_all('tr')
        region_rows = list(filter(lambda row: row.find('th', {'scope': 'row'}) is not None, rows))
        self.counts: [DailyCount] = list(map(lambda region: DailyCount(
            region=region.contents[0].text,
            overall=Common.to_number(region.contents[1].text),
            korea=Common.to_number(region.contents[2].text),
            overseas=Common.to_number(region.contents[3].text),
            rates_per_100k=Common.to_number(region.contents[7].text) / 100000,
        ), region_rows))

    def _find_severes(self, soup):
        total_map = soup.select('ul.cityinfo.total li')
        map_items = list(map(lambda item: MapItem(
            title=str(item.contents[0].text).strip(),
            count=Common.to_number(item.contents[1].text)
        ), total_map))
        self.severe: Optional[int] = None
        self.admitted: Optional[int] = None

        for item in map_items:
            if item.title == '재원 위중증':
                self.severe = item.count
            if item.title == '신규입원':
                self.admitted = item.count


if __name__ == '__main__':
    print(COVIDCrawlerByRegion().message)
