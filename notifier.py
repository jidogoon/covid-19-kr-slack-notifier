from covid_crawler import COVIDCrawler
from slack_helper import SlackHelper

if __name__ == '__main__':
    with open('hook_url.conf', 'r') as f:
        hook_url = f.read().strip()
        f.close()

    crawler = COVIDCrawler()
    when = crawler.when
    all_counts = crawler.counts
    counts_all = next(filter(lambda count: count.region == '합계', all_counts), None)
    counts_seoul = next(filter(lambda count: count.region == '서울', all_counts), None)
    counts_gg = next(filter(lambda count: count.region == '경기', all_counts), None)

    message = f'오늘의 대한민국 COVID-19 [{when}]\n\n' \
              f'전국: {counts_all.overall} (국내 {counts_all.korea}, 해외유입 {counts_all.overseas})\n' \
              f'서울: {counts_seoul.overall} (국내 {counts_seoul.korea}, 해외유입 {counts_seoul.overseas})\n' \
              f'경기: {counts_gg.overall} (국내 {counts_gg.korea}, 해외유입 {counts_gg.overseas})'

    slack = SlackHelper(hook_url=hook_url)
    slack.report_to_slack(message)
