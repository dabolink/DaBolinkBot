import socket
from requests import ConnectionError
import API.Twitch
import Objects.User
from time import sleep
import Objects.Message


def irc_send(bot, irc, message):
    irc.send("PRIVMSG #{} :{}\r\n".format(bot.channel, message))


def start(bot, q):
    if bot.debug:
        import sys
        sys.stderr = open('Logs/Errors/{}/In.txt'.format(bot.channel), 'w')
    botnick = None
    botowner = None
    server = None
    password = None
    port = None
    mods = []
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
        q.kill_.put(("KILL",))
    channel = bot.channel

    irc = socket.socket()
    irc.connect((server, port))
    irc.send("PASS %s\r\n" % password)
    irc.send("USER {} 0 * :{}\r\n".format(botnick, botowner))
    irc.send("NICK {}\r\n".format(botnick))
    irc.send("JOIN #{}\r\n".format(channel))
    irc.send("CAP REQ :twitch.tv/commands\r\n")
    irc.send("CAP REQ :twitch.tv/membership\r\n")
    sleep(1)
    irc_send(bot, irc, "/mods")
    try:
        chatters = API.Twitch.get_channel_viewers(bot.channel)["chatters"]
        print chatters
        for mod in chatters["moderators"]:
            q.var_queue.put(("VIEWER", "JOIN", Objects.User.User(mod, bot.start_time, True)))
        for viewer in chatters["viewers"]:
            q.var_queue.put(("VIEWER", "JOIN", Objects.User.User(viewer, bot.start_time, False)))
    except ConnectionError:
        while not chatters:
            chatters = API.Twitch.get_channel_viewers(bot.channel)
        chatters = chatters["chatters"]
        for mod in chatters["moderators"]:
            q.var_queue.put(("VIEWER", "JOIN", Objects.User.User(mod, bot.start_time, True)))
        for viewer in chatters["viewers"]:
            q.var_queue.put(("VIEWER", "JOIN", Objects.User.User(viewer, bot.start_time, False)))
    except TypeError:
        pass
    mods.append(bot.channel)
    print mods
    q.chat_queue.put(("MODS", mods))
    socket.setdefaulttimeout(5)
    while q.kill_queue.empty():
        msgData = irc.recv(2048)
        if len(msgData) == 0:
            print "msgData len = 0"
        i = 0
        try:
            while msgData.split("\n")[i]:
                msg = Objects.Message.Message(msgData.split("\r\n")[i], mods)
                if msg.type:
                    print msg.type
                    if msg.type == "PING":
                        q.out_queue.put(("PING",))
                        irc.send("PING time.twitch.tv\r\n")
                        print "PONG"
                    if msg.type == "MODS":
                        mods = msg.LoM
                        if bot.channel not in mods:
                            mods.append(bot.channel)
                    q.chat_queue.put((msg,))
                else:
                    print "que?"
                i += 1
            sleep(bot.sleep_time)
        except IndexError:
            pass
    print "IN"
