import aiohttp
import asyncio
from bs4 import BeautifulSoup


class Parameters:
    """
    The class to receive and store cmd line arguments.
    """
    def __init__(self, url):
        self.url = url


class RssReader:
    """
    The class to apply the core reader functions.
    """

    def __init__(self):
        self.rss_data = None
        self.rss_channel = None
        self.news_items = []
        self.news_content = []

    @staticmethod
    async def get_data(url: str) -> str:
        """
        Sends a http request and returns a response (string with XML or http data).
        :param url: URL to get info from.
        :return: String with raw webpage data.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    def parse_rss_data(self) -> None:
        """
        Processes XML data: structures, extracts channel name, news items and their features,
        then stores everything in RssReader instance attributes.
        :return: None. Updates class instance attrs.
        """
        extract = BeautifulSoup(self.rss_data, 'xml')
        self.rss_channel = extract.find('channel').find('description').text
        all_items = extract.find_all('item')   # BS data object

        for item in all_items:
            title = item.find('title').text
            date = item.find('pubDate').text
            link = item.find('link').text
            self.news_items.append({'Title': title, 'Date': date, 'Link': link})

    async def get_all_news(self) -> list:
        """
        Forms a pool of news links, retrieves all news content in async mode, extracts article texts.
        :return: List with texts of each news article
        """
        urls = [item['Link'] for item in self.news_items]
        tasks = []
        for url in urls:
            tasks.append(self.get_data(url))
        html_pages = await asyncio.gather(*tasks)  # Non-parsed pages
        return [self.parse_news(html) for html in html_pages]

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
        for item, content in zip(self.news_items, self.news_content):
            print(
                f"Feed: {self.rss_channel}\n",
                f"Title: {item['Title']}\n",
                f"Date: {item['Date']}\n",
                f"Article: {content}\n",
                f"Link: {item['Link']}",
                sep=''
            )
            print()


class Logger:
    pass


async def main():
    """
    Main event loop
    :return:
    """
    params = Parameters("https://feeds.bbci.co.uk/news/world/europe/rss.xml")   # Hardcoded/ Iteration 2
    reader = RssReader()
    reader.rss_data = await reader.get_data(params.url)
    reader.parse_rss_data()
    reader.news_content = await reader.get_all_news()
    reader.print_news()


asyncio.run(main())
