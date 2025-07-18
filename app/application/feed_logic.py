import asyncio
from asyncio import Queue
from concurrent.futures import ThreadPoolExecutor

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from app.domain.models import Feed, NewsItem


class FetchParseUseCase:
    """
    Use case that:
       reads xml from feed
       fetches the currently running loop (you asked for that!)
       ... and here comes MAGIC )))))
       I assume that parsing is CPU-heavy and want to delegate it to another thread.
       This requires bypassing GIL, and I do that with lxml parsing (C code, not Python).
       Thus, parsing is done by TPE thread and unblocks the loop - CONFIRMED.
    """

    def __init__(self, session: ClientSession, executor: ThreadPoolExecutor, feed_url: str):
        self.session = session
        self.executor = executor
        self.feed_url = feed_url

    async def execute(self) -> None:
        """
        Use case sequence execution.
        """
        xml_text = await self.fetch_feed()
        loop = asyncio.get_running_loop()
        parsed_feed = await loop.run_in_executor(self.executor, self.parse_feed, xml_text)
        self.print_feed(parsed_feed)

    async def fetch_feed(self) -> str:
        """
        Fetches XML by feed link
        """
        async with self.session.get(self.feed_url) as response:
            if response.status != 200:
                raise Exception("Server response error")
            return await response.text()

    @staticmethod
    def parse_feed(xml_text: str) -> Feed:
        """
        Parses XML, extracts name, description, pubdate, and news items.
        Returns Feed class with updated attributes.
        """
        extract = BeautifulSoup(xml_text, "lxml-xml")
        channel_name = extract.find("channel").find("title").text
        items = extract.find_all("item")  # BS data object
        parsed_feed = Feed(channel_name)

        for item in items:
            _link = item.find("link").text if item.find("link") else ""
            _title = item.find("title").text.replace("&nbsp;", " ") if item.find("title") else ""
            _date = item.find("pubDate").text if item.find("pubDate") else ""
            _description = item.find("description").text if item.find("description") else ""
            parsed_feed.news_items[_link] = NewsItem(title=_title, pubdate=_date, description=_description)

        return parsed_feed

    @staticmethod
    def print_feed(parsed_feed: Feed):
        """
        Just a simple stdout.
        """
        for key, value in parsed_feed.news_items.items():
            print(f"Title: {value.title}")
            print(f"Date: {value.pubdate}")
            print(f"Brief: {value.description}")
            print(f"More: {key}")
            print()


async def worker(queue: Queue, session: ClientSession, executor: ThreadPoolExecutor):
    """
    Worker.
    Gets url from the queue
    Checks if url is valid
    Calls the use case with some MAGIC and a timeout, and handles TimeoutError
    Says task_done() in any case.
    """
    while True:
        feed_url = await queue.get()
        try:
            if feed_url is None:
                break
            use_case = FetchParseUseCase(session, executor, feed_url)
            await asyncio.wait_for(use_case.execute(), timeout=5)
        except asyncio.TimeoutError:
            print(f"{feed_url} feed processing timed out.")
        finally:
            queue.task_done()
