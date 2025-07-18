"""
This module contains functions to export news data in various formats (initially - JSON).
"""

from pydantic import BaseModel
import json


class News(BaseModel):
    """
    pydantic DTO to store news info.
    """

    title: str
    date: str
    article: str


def save_as_json(data: dict, logger) -> None:
    """
    Saves news data into JSON file.
    :param data: RssFeed.news_items attr as dict ('link': News DTO)
    :param logger: logger instance.
    :return: None. JSON file created.
    """
    logger.info("Creating a JSON file...")
    json_data = {url: news.json() for url, news in data.items()}
    with open("rss_feed.json", "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
    logger.info("JSON file created")
