import asyncio

import aiohttp

from app.application.feed_logic import worker
from app.presentation.news_feeds import rss_feeds
from concurrent.futures import ThreadPoolExecutor

from app.presentation.rss_feeder import put_feed_into_queue


async def main(w_num):

    queue = asyncio.Queue(maxsize=5)
    executor = ThreadPoolExecutor(max_workers=5)

    async with aiohttp.ClientSession() as session:
        producer = asyncio.create_task(put_feed_into_queue(queue, rss_feeds, w_num))
        workers = [asyncio.create_task(worker(session, queue, executor)) for _ in range(w_num)]

        await producer
        await queue.join()
        executor.shutdown()


if __name__ == "__main__":
    num = 5  # Волшебное число воркеров от Володи
    asyncio.run(main(w_num=5))   # Под капотом run создает event loop