import aiohttp
import asyncio
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Parameters:
    """
    The class to receive and store cmd line arguments.
    """
    url: str
    to_json: bool = False
    limit: int = None


@dataclass
class News:
    """
    The dataclass to store news item structure
    """
    title: str
    date: str
    article: str


class RssReader:
    """
    The class to apply the core reader functions.
    """

    def __init__(self):
        self.rss_data = None
        self.rss_channel = None
        self.news_items = dict()

    @staticmethod
    async def get_data(url: str) -> str:
        """
        Sends a http request and returns a response (string with XML or http data).
        :param url: URL to get info from.
        :return: String with raw webpage data.
        """
        async with (aiohttp.ClientSession() as session):
            async with session.get(url, timeout=10) as response:
                return await response.text()

    def parse_rss_data(self) -> None:
        """
        Processes XML data: structures, extracts channel name, news items and their features,
        then stores everything in RssReader instance attributes.
        :return: None. Updates class instance attrs.
        """
        extract = BeautifulSoup(self.rss_data, 'xml')
        self.rss_channel = extract.find('channel').find('title').text
        all_items = extract.find_all('item')   # BS data object

        for item in all_items:
            _title = item.find('title').text
            _date = item.find('pubDate').text
            _link = item.find('link').text
            self.news_items[_link] = News(title=_title, date=_date, article="")

    async def get_all_news(self) -> None:
        """
        Forms a pool of news links and futures, retrieves all news content in async mode,
        extracts article texts.
        :return: None. Updates dataclass attributes.
        """
        tasks = {url: self.get_data(url) for url in self.news_items}
        html_pages = await asyncio.gather(*tasks.values())  # Non-parsed pages
        for url, html in zip(tasks.keys(), html_pages):
            self.news_items[url].article = self.parse_news(html)

    @staticmethod
    def parse_news(html) -> str:
        """
        Parses a page with the news article.
        :param html:  Non-parsed page from the parental function.
        :return: String with article text.
        """
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        if article:
            paragraphs = article.find_all('p')
            news_text = '\n'.join(paragraph.get_text() for paragraph in paragraphs)
            return news_text
        else:
            return 'No article available'   # How to cover all http structure types???

    def print_news(self):
        """
        Prints all feed content (to be upgraded).
        :return: None.
        """
        for key, value in self.news_items.items():
            print(
                f"Feed: {self.rss_channel}\n",
                f"Title: {value.title}\n",
                f"Date: {value.date}\n",
                f"Article: {value.article}\n",
                f"Link: {key}",
                sep=''
            )
            print()


async def main():
    """
    Main event loop
    :return:
    """
    params = Parameters("http://news.rambler.ru/rss/politics/")
    reader = RssReader()
    reader.rss_data = await reader.get_data(params.url)
    reader.parse_rss_data()
    await reader.get_all_news()
    reader.print_news()


asyncio.run(main())
