import asyncio
import collections
from asyncio import Queue
from typing import Any


async def put_feed_into_queue(queue: Queue, rss_feeds: Any, num: int):
    """
    Producer: puts feeds into the queue depending on the feed source type.
    For 'infinite' source: manual stopping required.
    For 'finite' source: adds None for each worker to stop them.
    """

    if rss_feeds is None:
        raise ValueError("No feed source found")

    if isinstance(rss_feeds, asyncio.Queue):
        while True:
            feed = await rss_feeds.get()
            await queue.put(feed)

    elif isinstance(rss_feeds, collections.abc.AsyncIterable):
        async for feed in rss_feeds:
            await queue.put(feed)

    else:
        for feed in rss_feeds:
            await queue.put(feed)

    for _ in range(num):
        await queue.put(None)
