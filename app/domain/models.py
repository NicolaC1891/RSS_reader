class Feed:
    """
    Feed class, stores feed name and a dict of items from XML.
    For future parsing of news texts if required.
    """
    def __init__(self, channel_name: str):
        self.channel_name: str = channel_name
        self.news_items: dict = {}


class NewsItem:
    """
    Class to store news item from XML feed.
    """
    def __init__(self, title: str, pubdate: str, description: str):
        self.title = title
        self.pubdate = pubdate
        self.description = description