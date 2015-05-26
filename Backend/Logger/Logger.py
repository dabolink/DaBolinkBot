import time
import API.Twitch
import Time.Time


def print_log(bot, type, message=None):
    t = time.strftime("%m-%d %H:%M", time.localtime())
    if type == "TIMEOUT":
        filename = "Logs/Timeouts/{}.txt".format(bot.channel)
    elif type == "DATABASE":
        filename = "Logs/Databases/{}.txt".format(bot.channel)
    elif type == "CHAT":
        filename = "Logs/Chats/{}.txt".format(bot.channel)
    elif type == "ERRORS":
        filename = "Logs/Errors/{}.txt".format(bot.channel)
    elif type == "BOOKMARK":
        filename = "Logs/Bookmarks/{}.txt".format(bot.channel)
        if not message:
            stream = API.Twitch.get_stream(bot.channel)["stream"]
            if stream:
                from time import gmtime
                cur_time = gmtime()
                bmtime = Time.Time.getTimeDiff(stream["created_at"], cur_time)
                message = str(bmtime) + "\n"
            else:
                message = "bookmark failed: stream not up"
    elif type == "COMMAND":
        filename = "Logs/Commands/{}.txt".format(bot.channel)
        if not message:
            message = type
    else:
        filename = "Logs/General/{}.txt".format(bot.channel)
    try:
        with open(filename, "a") as f:
            f.write("{} :> {}\n".format(t, message))
    except IOError:
        with open(filename, "w") as f:
            f.write("{} :> {}\n".format(t, message))

def start(bot, q):
    if bot.debug:
        import sys
        sys.stderr = open('Logs/Errors/{}/Logger.txt'.format(bot.channel), 'w')
    kill_secure = False
    while q.kill_queue.empty() or not kill_secure:
        if not q.log_queue.empty():
            var = q.log_queue.get()
            if var[0] == "KILL":
                kill_secure = True
            elif len(var) > 1:
                print_log(bot, var[0], var[1])
            else:
                print_log(bot, var[0])
        else:
            time.sleep(1)
    print "LOGGER"