"""
Task: Feed list from 0 to infinite elements.
Issue: List data structure does not support infinite elements.
Reasonable assumption: Infinite source is a queue or async iterable.
App logic: Cannot load the entire source at once (dynamic producer is required).
"""
import asyncio


async def infinite_source() -> str:
    """
    Mocking a replenishable feed source.
    Sleep prevents memory overload.
    """
    feed = "http://news.rambler.ru/rss/politics/"
    while True:
        await asyncio.sleep(0.1)
        yield feed


rss_feeds = ["https://feeds.bbci.co.uk/news/world/europe/rss.xml",
             "https://moxie.foxnews.com/feedburner/latest.xml",
             "https://feeds.simplecast.com/54nAGcIl",
             "http://news.rambler.ru/rss/politics/",
             "https://www.cbsnews.com/latest/rss/world",
             "https://www.buzzfeed.com/world.xml",
             "https://www.goha.ru/rss/mmorpg",
             "https://money.onliner.by/feed",
             "https://auto.onliner.by/feed",
             "https://cdn.feedcontrol.net/8/1114-wioSIX3uu8MEj.xml",
             "https://news.google.com/rss/",
             "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml",
             "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
             ]

# rss_feeds = []

# rss_feeds = infinite_source()
