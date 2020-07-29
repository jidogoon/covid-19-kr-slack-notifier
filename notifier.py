from covid_crawler import COVIDCrawler
from file_io import FileReader, FileWriter
from slack_helper import SlackHelper

LAST_WHEN_FILENAME = 'last_when'

if __name__ == '__main__':
    hook_urls = FileReader('hook_url.conf', default_value=None).read_lines()
    last_when = FileReader(LAST_WHEN_FILENAME, default_value=None).read()

    crawler = COVIDCrawler()
    when = crawler.when
    all_counts = crawler.counts
    counts_available = list(filter(lambda count: count.overall > 0, all_counts))
    counts_messages = list(map(lambda count: count.to_message(), counts_available))
    messages = '\n'.join(counts_messages)

    message = f'오늘의 대한민국 COVID-19 [{when}]\n\n' \
              f'{messages}'

    if last_when == when:
        exit(0)

    FileWriter(LAST_WHEN_FILENAME, when).write()
    for hook_url in hook_urls:
        slack = SlackHelper(hook_url=hook_url)
        slack.report_to_slack(message)
