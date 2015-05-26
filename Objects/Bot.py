import datetime


class Bot:
    def __init__(self, channel, debug=True):
        self.debug = debug
        self.channel = channel
        self.start_time = datetime.datetime.utcnow()
        self.timeout_time = 1
        self.offline_counter = 5