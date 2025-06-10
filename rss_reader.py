import aiohttp
import asyncio

urls = ["http://feeds.bbci.co.uk/news/world/europe/rss.xml", "https://www.onliner.by/feed"]


class RssReader:
    async def get_xml(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
                print(content)


async def main(urls):
    reader = RssReader()
    for url in urls:
        await reader.get_xml(url)

asyncio.run(main(urls))
