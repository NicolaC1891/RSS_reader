"""
This module contains the core RSS feed class to retrieve, parse, and store RSS feed info.
"""

import requests
from bs4 import BeautifulSoup
from from_old_project import data_storage as ds


class RssFeed:
    """
    Core class to retrieve and store RSS feed info and news items.
    """

    def __init__(self, link: str) -> None:
        """
        Initializes the class instance with URL.
        :param link: URL from params.
        """
        self.source = link
        self.content = None
        self.name = None
        self.news_items = dict()

    def get_rss_data(self, logger) -> str:
        """
        Sends an HTML request to RSS feed, returns response in text form.
        :param logger: logger instance.
        :return: String with response in text form if status 200.
        """
        logger.info("Fetching RSS feed...")
        response = requests.get(self.source)
        if response.status_code != 200:
            logger.info("RSS feed not fetched")
            raise requests.exceptions.RequestException("Server response error")
        logger.info("RSS feed fetched")
        return response.text

    def parse_rss_data(self, limit: int, logger) -> tuple[str, dict]:
        """
        Parses RSS feed data into channel name and list of news items
        :param limit: int value from params or None
        :param logger: logger instance
        :return: Tuple with channel name and news items dict {'link': News(title, date, article)}
        """
        logger.info("Parsing feed data...")
        extract = BeautifulSoup(self.content, "xml")
        channel_name = extract.find("channel").find("title").text
        items = extract.find_all("item")  # BS data object

        news_items = dict()
        if limit == 0:
            logger.info("No news to be fetched due to limit")
            return channel_name, news_items
        else:
            max_news = limit if limit else float("inf")

        for item in items:
            if len(news_items) < max_news:
                title = item.find("title").text.replace("&nbsp;", " ")
                date = item.find("pubDate").text
                link = item.find("link").text
                news_items[link] = ds.News(title=title, date=date, article="")
            else:
                break
        logger.info("RSS data parsed")
        return channel_name, news_items
