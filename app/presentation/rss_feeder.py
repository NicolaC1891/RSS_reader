import asyncio
import collections


async def put_feed_into_queue(queue, rss_feeds, num):
    """
    По условию задачи, источник фидов может быть:
    - пустым списком,
    - конечным списком,
    - бесконечным (это не список!)
    Условие не совсем корректно, бесконечный источник будет представлен скорее всего:
     - внешней очередью, где наш скрипт - консьюмер
     - асинхронным итерируемым объектом
     - хз чем еще, у меня нет опыта, чтобы это представить.

    Пишем функцию для охвата всего, о чем я мог подумать.
    Защита от None на случай некорректного вызова.

    Если источник фидов бесконечен - скрипт тоже бесконечен, ожидаемо.
    Если источник конечен - добавляем условия прерывания воркеров, т.к. они на трамплине.
    """

    if rss_feeds is None:
        raise ValueError("Источник фидов не найден")

    if isinstance(rss_feeds, asyncio.Queue):
        while True:
            feed = await rss_feeds.get()
            await queue.put(feed)

    elif isinstance(rss_feeds, collections.abc.AsyncIterable):
        async for feed in rss_feeds:
            await queue.put(feed)

    else:
        for feed in rss_feeds:
            print(f"Producer кладёт: {feed}")
            await queue.put(feed)

    for _ in range(num):
        print("Producer кладёт: None")
        await queue.put(None)
