from covid_crawler_base import COVIDCrawlerBase
from covid_crawler_by_hospital_bed import COVIDCrawlerByBed
from covid_crawler_by_region import COVIDCrawlerByRegion
from file_io import FileReader, FileWriter
from slack_helper import SlackHelper

LAST_WHEN_FILENAME_REGION = 'last_when_region'
LAST_WHEN_FILENAME_BED = 'last_when_bed'

hook_urls = FileReader('hook_url.conf', default_value=None).read_lines() or []


def notify(crawler: COVIDCrawlerBase, last_when_filename: str):
    last_when = FileReader(last_when_filename, default_value=None).read()
    when = crawler.when
    if last_when == when:
        return
    FileWriter(last_when_filename, when).write()
    for hook_url in hook_urls:
        slack = SlackHelper(hook_url=hook_url)
        slack.report_to_slack(crawler.message)


if __name__ == '__main__':
    notify(COVIDCrawlerByRegion(), LAST_WHEN_FILENAME_REGION)
    notify(COVIDCrawlerByBed(), LAST_WHEN_FILENAME_BED)
