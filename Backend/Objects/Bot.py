import datetime


class Bot:
    def __init__(self, channel, debug=True):
        self.debug = debug
        self.channel = channel
        self.start_time = datetime.datetime.utcnow()
        self.timeout_time = 1
        self.offline_counter = 5
        self.hello_message = "hello, i am DaBolinkBot, i am here to help moderate the chat"
        self.sleep_time = 0.5
        self.periodic_sleep = 30
        self.freq_viewer_time = 10
        self.freq_viewer_message = "Hey, You are a frequent viewer to this channel, stay tuned for more features coming soon"