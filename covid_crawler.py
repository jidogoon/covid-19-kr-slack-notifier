import requests
from bs4 import BeautifulSoup


class DailyCount:
    def __init__(self, region: str, overall: int, korea: int, overseas: int):
        self.region: str = region
        self.overall: int = overall
        self.korea: int = korea
        self.overseas: int = overseas


class COVIDCrawler:
    SOURCE_URL: str = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13'

    def __init__(self):
        req = requests.get(self.SOURCE_URL)
        soup = BeautifulSoup(req.text, 'html.parser')

        self.when = soup.find('p', {'class': 'info'}).text.strip()

        container = soup.find('div', {'class': 'mgt24'})
        rows = container.find_all('tr')
        region_rows = list(filter(lambda row: row.find('th', {'scope': 'row'}) is not None, rows))

        self.counts: [DailyCount] = []

        for region_row in region_rows:
            region_name = region_row.contents[0].text
            region_overall = region_row.contents[1].text
            region_overseas = region_row.contents[2].text
            region_korea = region_row.contents[3].text

            print(f'{region_name}|{region_overall}|{region_overseas}|{region_korea}')
            self.counts.append(DailyCount(
                region=region_name,
                overall=int(region_overall),
                korea=int(region_korea),
                overseas=int(region_overseas)
            ))


if __name__ == '__main__':
    _counts = COVIDCrawler().counts
    print(_counts)
