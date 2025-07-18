"""
Для теста взято 15 фидов, но я помню про оговорку "до бесконечности".
Считаем, что конец списка неизвестен.
Из этого вывод: грузить целиком в память не получится.
"""

rss_feeds = ["https://feeds.bbci.co.uk/news/world/europe/rss.xml",
             "https://moxie.foxnews.com/feedburner/latest.xml",
             "https://feeds.simplecast.com/54nAGcIl",
             "http://news.rambler.ru/rss/politics/",
             "https://www.cbsnews.com/latest/rss/world",
             "https://www.buzzfeed.com/world.xml",
             "https://www.goha.ru/rss/mmorpg",
             "https://money.onliner.by/feed",
             "https://auto.onliner.by/feed",
             "https://cdn.feedcontrol.net/8/1114-wioSIX3uu8MEj.xml",
             "https://news.google.com/rss/",
             "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml",
             "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
             ]