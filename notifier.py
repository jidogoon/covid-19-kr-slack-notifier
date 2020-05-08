from covid_crawler import COVIDCrawler
from slack_helper import SlackHelper

if __name__ == '__main__':
    with open('hook_url.conf', 'r') as f:
        hook_url = f.read().strip()
        f.close()

    crawler = COVIDCrawler()
    when = crawler.when
    all_counts = crawler.counts
    counts_available = list(filter(lambda count: count.overall > 0, all_counts))
    counts_messages = list(map(lambda count: count.to_message(), counts_available))
    messages = '\n'.join(counts_messages)

    message = f'오늘의 대한민국 COVID-19 [{when}]\n\n' \
              f'{messages}'

    slack = SlackHelper(hook_url=hook_url)
    slack.report_to_slack(message)
