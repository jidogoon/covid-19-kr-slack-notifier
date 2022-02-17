import re


class Common:
    @staticmethod
    def to_number(text: str) -> int:
        if text.strip() == '':
            return 0
        if not bool(re.search(r'\d', text)):
            return 0
        return int(re.sub(r'[^0-9]', '', text))
