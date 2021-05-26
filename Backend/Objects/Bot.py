import datetime
import sqlite3


class Bot:
    def __init__(self, channel, debug=True):
        self.sleep_time = 0.5
        self.periodic_sleep = 30
        self.offline_counter = 5
        self.start_time = datetime.datetime.utcnow()
        self.debug = debug
        self.channel = channel
        self.hello_message = "hello, i am DaBolinkBot, i am here to help moderate the chat"
        self.freq_viewer_message = "Hey, You are a frequent viewer to this channel, stay tuned for more features coming soon"

        conn = sqlite3.connect("Database/Master.db")
        cur = conn.cursor()
        result = cur.execute("""SELECT * FROM Channels WHERE channel = ?""", (channel,)).fetchone()
        if result:
            self.timeout_time = result[1]
            self.freq_viewer_time = result[2]
            self.follow_message = result[3]
        else:
            self.timeout_time = 1
            self.freq_viewer_time = 5
            self.follow_message = "new follower!!!! {} !!!! RAISE YOUR KAPPAS Kappa Kappa Kappa Kappa !!!!"
            cur.execute("""INSERT INTO Channels VALUES (?,?,?,?)""", (channel,self.timeout_time,self.freq_viewer_time,self.follow_message))