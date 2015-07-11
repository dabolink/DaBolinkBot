import socket
from time import sleep
links = True
cv = None


def irc_send_message(bot, irc, message):
    irc.send("PRIVMSG #{} :{}\r\n".format(bot.channel, message))


def irc_send_command(bot, irc, message):
    irc.send("PRIVMSG #{} :/{}\r\n".format(bot.channel, message))


def parse_output(bot, irc, output):
    global links
    if output[0] == "PRIVMSG":
        irc_send_message(bot, irc, output[1])
    elif output[0] == "TOGGLE":
        if len(output) == 1:
            links = not links
            if links:
                irc_send_message(bot, irc, "Link Timeout Enabled")
            else:
                irc_send_message(bot, irc, "Link Timeout Disabled")
        elif output[1]:
            links = True
            irc_send_message(bot, irc, "Link Timeout Enabled")
        else:
            links = False
            irc_send_message(bot, irc, "Link Timeout Disabled")
    elif output[0] == "PING":
        irc.send("PONG tmi.twitch.tv\r\n")
    elif output[0] == "TIMEOUT":
        if links:
            irc_send_message(bot, irc, "Please no links unless you are given permission")
            irc_send_command(bot, irc, "timeout {} {}".format(output[1], str(15)))
    elif output[0] == "MODS":
        print "mod request sent"
        irc_send_command(bot, irc, "mods")


def start(bot, q):
    import sys
    global links
    links = True
    if bot.debug:
        sys.stderr = open('Logs/Errors/{}/Out.txt'.format(bot.channel), 'w')
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
        q.kill_queue.put(("KILL",))
    channel = bot.channel

    irc = socket.socket()
    irc.connect((server, port))
    irc.send("PASS {}\r\n".format(password))
    irc.send("USER {} 0 * :{}\r\n".format(botnick, botowner))
    irc.send("NICK {}\r\n".format(botnick))
    irc.send("JOIN #{}\r\n".format(channel))
    irc_send_message(bot, irc, bot.hello_message)
    print "message sent"
    while q.kill_queue.empty():
        if not q.out_queue.empty():
            output = q.out_queue.get()
            parse_output(bot, irc, output)
        else:
            sleep(1)
    print "OUT"
    irc_send_message(bot, irc, "Goodbye Stream :(")
