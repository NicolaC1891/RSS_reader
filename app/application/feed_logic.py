import asyncio

import aiohttp
from bs4 import BeautifulSoup

from app.domain.models import Feed, NewsPiece


async def fetch_feed(session, url: str) -> str:
    async with session.get(url) as response:
        if response.status != 200:
            raise Exception("Server response error")  # С типами ошибок aiohttp разберусь позже.
        return await response.text()


def parse_feed(text: str) -> Feed:
    extract = BeautifulSoup(text, "lxml-xml")

    channel_name = extract.find("channel").find("title").text
    items = extract.find_all("item")  # BS data object

    parsed_feed = Feed(channel_name)

    for item in items:
        _link = item.find("link").text if item.find("link") else ""
        _title = item.find("title").text.replace("&nbsp;", " ") if item.find("title") else ""
        _date = item.find("pubDate").text if item.find("pubDate") else ""
        _description = item.find("description").text if item.find("description") else ""
        parsed_feed.news_items[_link] = NewsPiece(title=_title, pubdate=_date, description=_description)

    return parsed_feed


def print_feed(parsed_feed: Feed):
    for key, value in parsed_feed.news_items.items():
        print(f"Заголовок: {value.title}")
        print(f"Дата публикации: {value.pubdate}")
        print(f"Описание: {value.description}")
        print(f"Где почитать: {key}")
        print()


async def handle_feed(session, feed_url, executor):
    xml_text = await fetch_feed(session, feed_url)
    loop = asyncio.get_running_loop()
    parsed_feed = await loop.run_in_executor(executor, parse_feed, xml_text)
    print(f"parsed feed {feed_url}")
#    print_feed(parsed_feed)


async def worker(session, queue, executor):
    while True:
        feed_url = await queue.get()
        try:
            if feed_url is None:
                break
            await asyncio.wait_for(handle_feed(session, feed_url, executor), timeout=5)
            print(f"Worker finished task {feed_url}")
        except asyncio.TimeoutError:
            print(f"Обработка фида {feed_url} заняла слишком много времени — прервана")
        finally:
            queue.task_done()
