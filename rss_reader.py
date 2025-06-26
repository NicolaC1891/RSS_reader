import argparse
import requests
import feed_reader as fr
import news_parser as npar
import data_storage as ds
import logger as log
import asyncio


def read_params() -> argparse.Namespace:
    """
    Reads CLI parameters
    :return: argparge.Namespace instance with CLI parameters stored in attributes
    """
    parser = argparse.ArgumentParser(description="This is an RSS reader")
    parser.add_argument("--source", type=str, help="RSS URL")  # remove --
    parser.add_argument("--version", action="version", version="RSS Reader v.0.1")
    parser.add_argument("--json", action="store_true", help="Print results as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Output verbose status messages")
    parser.add_argument("--limit", type=int, help="Limit new topics if this parameter is provided")
    return parser.parse_args()


def main():
    """
    Main app function
    """

    logger = log.create_logger()

    # Read CLI parameters // set manually for integration testing
    params = read_params()
    params.source = "https://auto.onliner.by/feed"
    params.verbose = True
    params.limit = 5
    params.json = True
    log.setup_logger(params.verbose)
    logger.info("Program launched")

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
    main()
