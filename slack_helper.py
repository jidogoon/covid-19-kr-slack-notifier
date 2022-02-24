import json
import requests


class SlackHelper:
    def __init__(self, hook_url: str):
        self.hook_url = hook_url

    def report_to_slack(self, content: str):
        print(f'send using hook url = {self.hook_url}\nmsg = {content}')
        if self.hook_url is None or self.hook_url.strip() == '':
            raise Exception('check conf!')

        payload = {"text": content}

        requests.post(
            self.hook_url, data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
