import re
import Objects.User
import datetime


class Message:
    def __init__(self, message, mods=[]):
        self.message = None
        self.type = None
        self.url = False
        # :jtv!jtv@jtv.tmi.twitch.tv PRIVMSG dabolinkbot :The moderators of this room are: m00nski, dabolink, jrkyex, raverfx, dabolinkbot, thepretenderr
        result1 = re.match(r":(\S+)!(\S+)@(\S*).tmi.twitch.tv (\S+) [#]?((\w+)(\r)?)?( :(.+))?", message)
        result2 = re.match(":tmi.twitch.tv (.*) (.*) :(.+)", message)
        result3 = re.match(r":jtv MODE #(.*) ([+]|[-])o (.+)", message)
        result4 = re.match(r":(.*).tmi.twitch.tv(.*)", message)
        if result1:
            self.type = result1.group(4)
            if result1.group(1) in mods:
                self.user = Objects.User.User(result1.group(1), datetime.datetime.utcnow(), True)
            else:
                self.user = Objects.User.User(result1.group(1), datetime.datetime.utcnow(), False)
            if result1.group(4) == "JOIN":
                self.type = "JOIN"

            elif result1.group(4) == "PRIVMSG":
                self.message = result1.group(9).lower()
                if result1.group(5):
                    result5 = re.match(".*(http(s)?://)?(www.)?\p{L}+[.]\p{L}\p{L}+(/\p{L}*)?.*", self.message)
                    result6 = re.match("the moderators of this room are: (.+)", self.message)
                    if result5 or "RAF2" in self.message:
                        self.url = True
                    elif result6 and self.user.name == "jtv":
                        self.type = "MODS"
                        self.LoM = result6.group(1).split(", ")

            elif result1.group(4) == "PART":
                self.type = "PART"
            else:
                print "unhandled1"

        elif result2:
            print "twitch message"

        elif result3:
            self.user = Objects.User.User(result3.group(3), datetime.datetime.utcnow(), True)
            self.type = "ADMIN"

        elif result4:
            print "result4"

        elif message[:4] == "PING":
            self.type = "PING"
            pass
        else:
            print "unhandled2"