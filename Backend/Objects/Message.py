import re
import Objects.User
import datetime


class Message:
    def __init__(self, message, mods=[]):
        self.message = None
        self.type = None
        self.url = False
        result1 = re.match(r":(\S+)!(\S+)@(\S*).tmi.twitch.tv (\S+) [#]?((\w+)(\r)?)?( :(.+))?", message)
        result2 = re.match(r":tmi.twitch.tv (.*) (.*) :(.+)", message)
        result3 = re.match(r":jtv MODE #(.*) ([+]|[-])o (.+)", message)
        result4 = re.match(r":tmi.twitch.tv (.*)", message)
        print message
        if result1:
            if result1.group(1) in mods:
                self.user = Objects.User.User(result1.group(1), datetime.datetime.utcnow(), True)
            else:
                self.user = Objects.User.User(result1.group(1), datetime.datetime.utcnow(), False)
            if result1.group(4) == "JOIN":
                self.type = "JOIN"
            elif result1.group(4) == "PRIVMSG":
                self.message = result1.group(9)
                print self.message
                self.type = "PRIVMSG"
            elif result1.group(4) == "PART":
                self.type = "PART"
            else:
                print "unhandled1"

        elif result2:
            self.message = result2.group(3).lower()
            print self.message
            self.type = "TWITCH"
            result6 = re.match("the moderators of this room are: (.+)", self.message)
            if result6:
                self.LoM = result6.group(1).split(", ")
                self.type = "MODS"
        elif result3:
            self.user = Objects.User.User(result3.group(3), datetime.datetime.utcnow(), True)
            self.type = "ADMIN"

        elif result4:
            print "else"

        elif message[:4] == "PING":
            self.type = "PING"
        else:
            print "unhandled2"

    def is_link(self):
        if self.message:
            link = re.match(".*(http(s)?://)?(www.)?[a-zA-Z]+[.][a-zA-Z]+(/[a-zA-Z]*)?.*", self.message)
        return False
