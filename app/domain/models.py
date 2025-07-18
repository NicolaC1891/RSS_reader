class Feed:
    """
    Класс для фида, хранит название и новостные итемы в виде инстансов NewsPiece.
    Это для парсинга самих новостей, если понадобится.
    """
    def __init__(self, channel_name: str):
        self.channel_name: str = channel_name
        self.news_items: dict = {}


class NewsPiece:
    """
    Класс для новости с основными атрибутами, содержащимися в рсс-фиде.
    """
    def __init__(self, title, pubdate, description):
        self.title = title
        self.pubdate = pubdate
        self.description = description