import requests
from bs4 import BeautifulSoup


class DailyCount:
    def __init__(self, region: str, overall: int, korea: int, overseas: int):
        self.region: str = region
        self.overall: int = overall
        self.korea: int = korea
        self.overseas: int = overseas

    def to_message(self):
        return f'{self.region}: {self.overall:,} (국내 {self.korea:,}, 해외유입 {self.overseas:,})'


class COVIDCrawler:
    SOURCE_URL: str = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13'

    def __init__(self):
        req = requests.get(self.SOURCE_URL)
        soup = BeautifulSoup(req.text, 'html.parser')

        self.when = soup.find('p', {'class': 'info'}).text.strip()

        container = soup.find('div', {'class': 'mgt24'})
        rows = container.find_all('tr')
        region_rows = list(filter(lambda row: row.find('th', {'scope': 'row'}) is not None, rows))

        self.counts: [DailyCount] = list(map(lambda region: DailyCount(
            region=region.contents[0].text,
            overall=int(region.contents[1].text.replace(',', '')),
            korea=int(region.contents[2].text.replace(',', '')),
            overseas=int(region.contents[3].text.replace(',', ''))
        ), region_rows))


if __name__ == '__main__':
    _counts = COVIDCrawler().counts
    print(_counts)
