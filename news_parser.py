"""
This module contains functions to retrieve and parse html of each separate news item from RSS feed.
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re


async def get_news(feed, logger) -> tuple[str]:
    """
    Forms a pool of news links and futures, retrieves all news content in async mode,
    extracts article texts.
    :return: None. Updates dataclass attributes.
    """
    logger.info("Fetching news articles asynchronously...")
    tasks = {url: fetch_news(url, logger) for url in feed.news_items}
    html_pages = await asyncio.gather(*tasks.values())  # Non-parsed pages
    logger.info("All articles fetched")
    return html_pages


async def fetch_news(url: str, logger) -> str:
    """
    Sends an HTML request to a news page and retrieves response text
    :param url: String with URL address of the news item
    :param logger: logger instance
    :return: String with response text
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            match response.status:
                case 200:
                    logger.info(f"Article fetched (url: {url})")
                    return await response.text()
                case _:
                    logger.error(f"Error fetching article ({url})")
                    return f"Unable to retrieve the article: status {response.status}"


def parse_news(html: str) -> str:
    """
    Parses an HTML response text, selects and refines text paragraphs, joins into news article.
    :param html: String with HTML response text.
    :return: String with news article text.
    """
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")
    news_text = " ".join(paragraph.get_text() for paragraph in paragraphs)
    clean_text = re.sub(r"\n+", " ", news_text)
    clean_text = re.sub(r"\s{2,}", " ", clean_text)

    if clean_text:
        return f"{clean_text[:400]}[...]"
    else:
        return "[...]"
