import asyncio

import aiohttp

from app.infrastructure.logger import logger
from app.infrastructure.feed_source import rss_feeds
from concurrent.futures import ThreadPoolExecutor

from app.presentation.producer import put_feed_into_queue
from app.application.feed_logic import worker


async def main(w_num: int):
    """
    Starts a queue.
    Creates an executor (see MAGIC in worker:)))
    In the session context:
      registers producer task
      registers worker tasks

      awaits producer - so that producer starts putting feeds into queue before join()
      awaits join() - waits until queue is empty (worker takes a task and does task_done())

      If source is 'finite' - workers will stop at None.
      If source is 'infinite' - my solution is stopping by timeout. There may be options.
    """

    queue = asyncio.Queue(maxsize=w_num)
    executor = ThreadPoolExecutor(max_workers=w_num)

    async with aiohttp.ClientSession() as session:
        producer = asyncio.create_task(put_feed_into_queue(queue, rss_feeds, w_num))
        workers = [asyncio.create_task(worker(queue, session, executor)) for _ in range(w_num)]

        await producer
        await queue.join()

        for _worker in workers:
            try:
                await asyncio.wait_for(_worker, timeout=20)
            except TimeoutError:
                logger.info("No available feeds. Stopping worker manually")
                _worker.cancel()

        executor.shutdown()


if __name__ == "__main__":
    num = 5  # Magic number of workers by Vladimir
    asyncio.run(main(w_num=5))
