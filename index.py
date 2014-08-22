#!/usr/bin/env python
from daemon import runner
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Status
from json import loads
from subprocess import call
import os.path
import urllib

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = "cFec8DIlKzEMJYEh0Q1HLDn7s"
consumer_secret = "wZ0yU2pV282kBdJ32PjjBxZgkIQp1oFT7GW0JZMgejt4SlocXu"
# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "2423666970-MLQQUFsaKm5oi83KSzoCOAKP1CWwcXX9yYjvERv"
access_token_secret = "JWk7aSuKOg6uefQvMH2X88ZUS9bmumi5yWwGca4fcD23z"


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, timelines):
        self.timelines = timelines
        super(StdOutListener, self).__init__()

    def on_data(self, data):
        tweet = loads(data)
        print tweet['user']['id_str'] + ' ' + tweet['user']['name']
        if any(tweet['user']['id_str'] in s for s in self.timelines):
            icon = self.get_icon(tweet['user']['profile_image_url'], tweet['user']['id_str'])
            call(["notify-send", tweet['user']['name'], tweet['text'], '-i',
                  icon])
        return True

    def on_error(self, status):
        print status

    @staticmethod
    def get_icon(url, name):
        ext = '.' + url.split('.')[-1]
        folder = os.path.dirname(os.path.abspath(__file__)) + '/icons/'
        path = folder + name + ext
        if os.path.isfile(path) is not True:
            urllib.urlretrieve(url, path)
        return path


class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/foo.pid'
        self.pidfile_timeout = 5

    @staticmethod
    def run():
        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)
        stream.filter(follow=['1454734730'])


if __name__ == '__main__':
    timelines = ['109516988', '1454734730', '1178067301']
    l = StdOutListener(timelines)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(follow=timelines)
    # app = App()
    # daemon_runner = runner.DaemonRunner(app)
    # daemon_runner.do_action()