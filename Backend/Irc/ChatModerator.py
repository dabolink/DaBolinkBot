from time import sleep


def start(bot, q):
    mods = []
    frequent_viewers = []
    if bot.debug:
        import sys
        sys.stderr = open('Logs/Errors/{}/ChatModerator.txt'.format(bot.channel), 'w')
    print "chat moderator staring up"
    while mods == [] or frequent_viewers == []:
        # print mods, frequent_viewers
        if not q.chat_queue.empty():
            msg = q.chat_queue.get()
            if msg[0] == "MODS":
                mods = msg[1]
                print "mods got"
            elif msg[0] == "VIEWERS":
                frequent_viewers = msg[1]
                print "viewers got"
        else:
            sleep(bot.sleep_time)
    print "chat moderator started"
    print mods, frequent_viewers
    while q.kill_queue.empty():
        if not q.chat_queue.empty():
            msg = q.chat_queue.get()[0]
            print msg
            if msg.type:
                if msg.type == "PRIVMSG":
                    print repr(msg.message)
                    q.log_queue.put(("CHAT", "<" + msg.user.name + "> " + msg.message))
                    if msg.message[0] == "!":
                        #is command
                        print "is command"
                        command = msg.message.split(" ")
                        q.command_queue.put((msg.user, command))
                    else:
                        if not msg.user.name == "dabolinkbot":
                            print "<{}>{}".format(msg.user.name, repr(msg.message))
                            if len(msg.message) >= 10:
                                q.database_queue.put(("incLOT", msg.user.name))
                    if msg.is_link():
                        print "link found"
                        q.log_queue.put(("LOG", msg.user.name + " posted a link: " + msg.message))
                        if not (msg.user.name in mods or msg.user.name in frequent_viewers):
                            q.var_queue.put(("PERMIT", "-", msg.user.name))
                    else:
                        print "no link"
                elif msg.type == "MODS":
                    mods = msg.LoM
                    print mods
                    if bot.channel not in mods:
                        mods.append(bot.channel)
                    q.var_queue.put(("MODS", mods))
                    print "mods updated"
                elif msg.type == "JOIN" or msg.type == "PART":
                    q.var_queue.put(("VIEWER", msg.type, msg.user))
                elif msg.type == "NOTICE":
                    pass
                elif msg.type == "PING":
                    print "PONG"
                    q.out_queue.put(("PING",))
                elif msg.type == "ADMIN":
                    if not mods.__contains__(msg.user.name):
                        mods.append(msg.user.name)
                        q.var_queue.put(("MODS", mods))
                else:
                    print msg
        else:
            sleep(bot.sleep_time)
    print "CHAT MODERATOR"
