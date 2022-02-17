from abc import ABC, abstractmethod


class COVIDCrawlerBase(ABC):
    when: str = None

    @property
    @abstractmethod
    def message(self) -> str:
        pass
