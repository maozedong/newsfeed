#!/usr/bin/python
import time
from daemon import runner
from datetime import datetime, timedelta
from subprocess import call
from operator import attrgetter
import feedparser


class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class Feed:
    t_mask = 'false'
    url = 'no url'

    def __init__(self):
        self.feed = feedparser.parse(self.url)


class NewsLigaNetFeed(Feed, object):
    t_mask = '%a, %d %b %Y %H:%M:%S +0300'
    url = "http://news.liga.net/all/rss.xml"
    icon = '/var/www/newsfeed/icons/NewsLigaNet.png'

    def getNews(self, fromDate):
        news = []
        # self.feed.entries.append(Bunch(published=datetime.now().strftime(t_mask), title='Test', summary='Test body'))
        for entrie in self.feed.entries:
            date = datetime.strptime(entrie.published, self.t_mask)
            if date > fromDate:
                news.append(FeedItem(date, entrie.title, entrie.summary, self.icon))
        return news


class LbUaFeed(Feed, object):
    t_mask = '%a, %d %b %Y %H:%M:%S +0300'
    url = "http://lb.ua/export/rss_news.xml"
    icon = '/var/www/music_network/newsfeed/icons/LbUa.jpg'

    def getNews(self, fromDate):
        news = []
        dates = []
        for entrie in self.feed.entries:
            date = datetime.strptime(entrie.published, self.t_mask)
            dates.append(entrie.published)
            if date > fromDate:
                news.append(FeedItem(date, entrie.title, entrie.summary, self.icon))
        return news


class FeedItem(object):
    def __init__(self, date, title, body, icon='/var/www/newsfeed/icons/breaking_news.jpg'):
        self.date = date
        self.title = title
        self.body = body
        self.icon = icon



def mainLoop():
    url = 'http://news.liga.net/all/rss.xml'
    iteration = 0
    t_mask = '%a, %d %b %Y %H:%M:%S +0300'
    last = datetime.now() - timedelta(hours=1)
    feeds = [NewsLigaNetFeed, LbUaFeed]
    while 1:
        news = []
        for feed in feeds:
            feed_obj = feed()
            part = feed_obj.getNews(last)
            news = news + part
        news = sorted(news, key=attrgetter('date'))
        for item in news:
            call(["notify-send", item.title, item.body, '-i',
                  item.icon])
        last = datetime.now()
        iteration += 1
        print datetime.now().strftime("%H:%M:%S") + ' ' + unicode(iteration) + ' iterations complete. ' + unicode(
            len(news)) + ' new articles'
        time.sleep(60)


class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/foo.pid'
        self.pidfile_timeout = 5

    def run(self):
        mainLoop()


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()