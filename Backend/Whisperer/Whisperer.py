import socket
from time import sleep


def irc_send_whisper(irc, user, message):
    irc.send("PRIVMSG #jtv :/w {} {}\r\n".format(user, message))
    print "sent whisper to", user, ":", message


def irc_send_message(channel, irc, message):
    irc.send("PRIVMSG #{} :{}\r\n".format(channel, message))
    print "sent message"


def start(bot, q):
    import sys
    if bot.debug:
        sys.stderr = open('Logs/Errors/{}/WhispererOut.txt'.format(bot.channel), 'w')
    botnick = None
    botowner = None
    server = None
    password = None
    port = None
    with open("ValuesWhisper.txt") as f:
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
            elif key == "Channel":
                channel = val
    if not (password and botnick and botowner and server and port and channel):
        q.kill_queue.put(("KILL",))
        print "whisper kill"
        exit()

    irc = socket.socket()
    irc.connect((server, port))
    irc.send("PASS {}\r\n".format(password))
    irc.send("USER {} 0 * :{}\r\n".format(botnick, botowner))
    irc.send("NICK {}\r\n".format(botnick))
    irc.send("JOIN #{}\r\n".format(channel))
    print "Whisper started"
    q.whisper_queue.put((bot.channel, "Hello, I am here to help moderate the chat :D"))
    while q.kill_queue.empty():
        if not q.whisper_queue.empty():
            output = q.whisper_queue.get()
            if output == "PONG":
                irc.send("PONG tmi.twitch.tv\r\n")
            else:
                recipient = output[0]
                message = output[1]
                irc_send_whisper(irc, recipient, message)
        else:
            sleep(bot.sleep_time)
    print "WHISPER"
