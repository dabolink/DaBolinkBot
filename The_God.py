import socket, time, re, multiprocessing
import Controller

irc = socket.socket()
Channel = "dabolinkbot"

def print_log(s):
    t = time.strftime("%m-%d %H:%M", time.localtime())
    try:
        with open("Logs/master_log.txt", "a") as f:
            f.write("{} :> {}\n".format(t, s))
    except IOError:
        with open("Logs/master_log.txt", "w") as f:
            f.write("{} :> {}\n".format(t, s))

class message:
    def __init__(self, message):
        self.message = None
        result1 = re.match("^:(\S+)!(\S+)@(\S*).tmi.twitch.tv (\S+) (#(\w+)(\r)?)?( :(.+))?$", message)
        result2 = re.match("^:tmi.twitch.tv (.*) (.*) :(.*)$", message)
        result3 = re.match("^:jtv MODE #(.*) (\+|\-)o (.*)", message)
        result4 = re.match("^:(.*).tmi.twitch.tv(.*)", message)
        print message
        if result1:
            self.user = result1.group(1)
            if result1.group(4) == "PRIVMSG":
                self.message = result1.group(9)
            else:
                pass

        elif result2:
            pass

        elif result3:
            pass

        elif result4:
            pass

        elif message[:4] == "PING":
            irc.send("PONG tmi.twitch.tv\r\n")
        else:
            pass

            #
            # else:
            #     self.user = message.split(":")[1].split("!")[0]
            #     self.type = message.split(" ")[1]
            #     if self.type == "PRIVMSG":
            #         self.message = message.split(":")[2]
            #     if not users.__contains__(self.user):
            #         users.append(self.user)
            #         irc_send("Hello " + self.user + " and welcome to the chat")
            #     if type == "PART":
            #         print "goodbye"


def irc_send(message):
    irc.send("PRIVMSG #{} :{}\r\n".format(Channel, message))

def main():
    processes = []

    botnick = None
    botowner = None
    server = None
    password = None
    port = None
    with open("Values.txt") as f:
        for line in f:
            (key, val) = line.split()
            if key == "Oauth":
                password = val
            elif key == "Botnick":
                botnick = val
            elif key == "Botowner":
                botowner = val
            elif key == "Server":
                server = val
            elif key == "Port":
                port = int(val)
    if not (password and botnick and botowner and server and port):
        exit()

    channel = "#{}".format(Channel)
    print "Establishing connection to [{}]".format(server)

    ##connecting
    irc.connect((server, port))
    irc.send("PASS {}\r\n".format(password))
    irc.send("USER {} 0 * :{}\r\n".format(botnick, botowner))
    irc.send("NICK {}\n".format(botnick))
    irc.send("JOIN {}\n".format(channel))
    print "Connected"
    while 1:
        msgData = irc.recv(2048)
        i = 0
        while msgData.split("\n")[i]:
            processes2 = []
            for p in processes:
                if p[2].is_alive():
                    processes2.append(p)
                else:
                    print_log("bot has been removed from channel #{}".format(p[0]))
            processes = processes2
            pflag = False
            msg = message(msgData.split("\r\n")[i])
            if msg.message:
                if msg.message[0] == "!":
                    if msg.message[1:4] == "add":
                        if len(msg.message) == 4:
                            chatroom = msg.user
                        else:
                            chatroom = msg.message.split(" ")[1]
                        for p in processes:
                            if p[0] == chatroom:
                                irc_send("#{} already has a bot in it".format(chatroom))
                                pflag = True
                        if not pflag:
                            if chatroom.endswith("s"):
                                irc_send("starting bot in {} chat".format(chatroom))
                            else:
                                irc_send("starting bot in: {}'s chat".format(chatroom))
                            if len(msg.message.split(" ")) > 2:
                                p = multiprocessing.Process(target=Controller.startup, args=(chatroom, False))
                            else:
                                p = multiprocessing.Process(target=Controller.startup, args=(chatroom, True))
                            p.start()
                            processes.append((chatroom, msg.user, p))
                            print_log("{} added bot to #{}".format(msg.user, chatroom))
                    else:
                        print "INVALD CMD"
                else:
                    print "<{}> {}".format(msg.user, msg.message)
            i += 1
        time.sleep(1)





if __name__ == "__main__":
    main()
