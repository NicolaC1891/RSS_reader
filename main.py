import feed_reader as fr
import news_parser as npar
import data_storage as ds
from logger import logger
import asyncio


def main():
    """
    Main app function
    """
    rss_feeds = [

    ]



    rss_feed = fr.RssFeed(params.source)

    try:
        rss_feed.content = rss_feed.get_rss_data(logger=logger)
    except requests.exceptions.RequestException as e:
        logger.error(f"Unable to access RSS feed: {e}")
        logger.info("Program terminated")
        return

    rss_feed.name, rss_feed.news_items = rss_feed.parse_rss_data(params.limit, logger=logger)

    html_news = asyncio.run(npar.get_news(rss_feed, logger=logger))

    logger.info("Parsing articles...")
    for url, html in zip(rss_feed.news_items, html_news):
        rss_feed.news_items[url].article = npar.parse_news(html)
    logger.info("Added article texts to news dataclasses")

    if params.json:
        ds.save_as_json(rss_feed.news_items, logger=logger)

    for key, value in rss_feed.news_items.items():
        print(value.title, value.date, value.article, key, sep="\n")
        print()

    logger.info("Program ended")


if __name__ == "__main__":
    logger.info("Program launched")
    main()
