from time import sleep
from Irc.other_functions import insert, binary_search


def start(bot, q):
    mods = None
    frequent_viewers = None
    banned_words = []
    if bot.debug:
        import sys
        sys.stderr = open('Logs/Errors/{}/ChatModerator.txt'.format(bot.channel), 'w')
    print "chat moderator staring up"
    while mods == None and frequent_viewers == None:
        if not q.chat_queue.empty():
            msg = q.chat_queue.get()
            if msg[0] == "MODS":
                mods = msg[1]
                print "mods got"
            elif msg[0] == "VIEWERS":
                frequent_viewers = []
                print "msg[1]", msg[1]
                for user in msg[1]:
                    frequent_viewers = insert(frequent_viewers, user)
                print frequent_viewers
                print "viewers got"
        else:
            sleep(bot.sleep_time)
    print "freq viewers: ", frequent_viewers
    print "chat moderator started"
    print mods, frequent_viewers
    while q.kill_queue.empty():
        if not q.chat_queue.empty():
            msg = q.chat_queue.get()
            if msg[0] == "MODS":
                mods = msg[1]
            elif msg[0] == "BANNED":
                banned_words = msg[1]
            elif msg[0].type:
                msg = msg[0]
                if msg.type == "PRIVMSG":
                    q.log_queue.put(("CHAT", "<" + msg.user.name + "> " + msg.message))
                    if msg.message[0] == "!":
                        if msg.message == "!print freq_viewers":
                            print frequent_viewers
                            q.out_queue.put(("PRIVMSG", str(frequent_viewers)))
                        print "command found"
                        command = msg.message.split(" ")
                        print command
                        q.command_queue.put((msg.user, command))
                    else:
                        if not msg.user.name == "dabolinkbot":
                            print "<{}> {}".format(msg.user.name, repr(msg.message))
                            if len(msg.message) >= 10:
                                q.database_queue.put(("incLOT", msg.user.name))
                            for word in banned_words:
                                if word in msg.message:
                                    print "banned word found"
                                    q.log_queue.put(("LOG", msg.user.name + " used a banned word: " + msg.message))
                                    q.out_queue.put(("TIMEOUT", "WORD", msg.user.name))
                    if msg.is_link():
                        print "link found:", msg.message
                        q.log_queue.put(("LOG", msg.user.name + " posted a link: " + msg.message))
                        if not (msg.user.name in mods or binary_search(frequent_viewers, msg.user.name)):
                            q.var_queue.put(("PERMIT", "-", msg.user.name))
                elif msg.type == "MODS":
                    mods = msg.LoM
                    if bot.channel not in mods:
                        mods.append(bot.channel)
                    print mods
                    q.var_queue.put(("MODS", mods))
                    print "mods updated"
                elif msg.type == "JOIN" or msg.type == "PART":
                    q.var_queue.put(("VIEWER", msg.type, msg.user))
                    print frequent_viewers, msg.user.name
                    if binary_search(frequent_viewers, msg.user.name) and msg.type == "JOIN":
                        q.whisper_queue.put((msg.user.name, bot.freq_viewer_message))
                elif msg.type == "NOTICE":
                    pass
                elif msg.type == "PING":
                    print "PONG"
                    q.out_queue.put(("PING",))
                    q.whisper_queue.put("PING")
                elif msg.type == "ADMIN":
                    if not mods.__contains__(msg.user.name):
                        mods.append(msg.user.name)
                        q.var_queue.put(("MODS", mods))
                else:
                    print msg.message
        else:
            sleep(bot.sleep_time)
    print "CHAT MODERATOR"
