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
    socket.setdefaulttimeout(5)
    while q.kill_queue.empty():
        msgData = irc.recv(2048)
        print msgData
        i = 0
        try:
            while msgData.split("\n")[i]:
                msg = Objects.Message.Message(msgData.split("\r\n")[i], mods)
                if msg.type == "PRIVMSG":
                    if not msg.user.admin and msg.url:
                        q.var_queue.put(("PERMIT", "-", msg.user.name))
                        q.log_queue.put(("LOG", msg.user.name + " posted a link: " + msg.message))
                    if msg.message:
                        q.log_queue.put(("CHAT", "<" + msg.user.name + "> " + msg.message))
                        if msg.message[0] == "!":
                            command = msg.message.split(" ")
                            q.command_queue.put((msg.user, command))
                        else:
                            if not msg.user.name == "dabolinkbot":
                                print "<{}>{}".format(msg.user.name, repr(msg.message))
                            if len(msg.message) >= 10:
                                q.database_queue.put(("incLOT", msg.user.name))
                elif msg.type == "JOIN" or msg.type == "PART":
                    q.var_queue.put(("VIEWER", msg.type, msg.user))
                elif msg.type == "PING":
                    q.out_queue.put(("PING",))
                    irc.send("PONG tmi.twitch.tv\r\n")
                    print "PONG"
                elif msg.type == "MODS":
                    if bot.channel not in msg.LoM:
                        msg.LoM.append(bot.channel)
                    q.var_queue.put(("MODS", msg.LoM))
                    mods = msg.LoM
                    print "mods updated"
                elif msg.type == "ADMIN":
                    if not mods.__contains__(msg.user.name):
                        mods.append(msg.user.name)
                        q.var_queue.put(("MODS", mods))
                i += 1
            sleep(1)
        except IndexError:
            pass
    print "IN"
