from time import sleep


def start(bot, q):
    if bot.debug:
        import sys
        sys.stderr = open('Logs/Errors/{}/ChatModerator.txt'.format(bot.channel), 'w')
    while q.kill_queue.empty():
        if not q.chat_queue.empty():
            msg = q.chat_queue.get()
            type = msg[0]
            params = msg[1:]
            if type == "PRIVMSG":
                pass
            elif type == "NOTICE":
                pass
            elif type == "":
                print "hi"
            else:
                print msg
        else:
            sleep(1)
    print "COMMAND PARSER"