import datetime
from time import sleep
import API.Twitch

global follower_queue, nonfollower_queue, followers, viewers, mods

def get_next():
    global follower_queue, nonfollower_queue, followers, viewers
    if len(follower_queue) > 0:
        u = follower_queue[0]
        follower_queue = follower_queue[1:]
        return u
    else:
        if len(nonfollower_queue) > 0:
            u = nonfollower_queue[0]
            nonfollower_queue = nonfollower_queue[1:]
            return u
        else:
            return None


def isFollower(user):
    global followers
    if user in followers:
        return True
    return False


def start(bot, q):
    if bot.debug:
        import sys
        sys.stderr = open('Logs/Errors/' + bot.channel + "/VarManager.txt", 'w')
    global follower_queue, nonfollower_queue, followers, viewers, mods
    follower_queue = []
    nonfollower_queue = []
    followers = []
    viewers = []
    mods = []
    permits = {}
    permits["dabolink"] = 1
    cv = None
    while q.kill_queue.empty():
        if not q.var_queue.empty():
            var = q.var_queue.get()
            if var[0] == "QUEUE":
                if var[1] == "GET":
                    get = get_next()
                    string = ""
                    if get:
                        string =  "next up... THE AMAZING: " + get
                    else:
                        string = "there is no one left in line"
                    q.out_queue.put(("PRIVMSG", string))
                    pass
                elif var[1] == "PUT":
                    # ("QUEUE", "PUT", user, u)
                    if isFollower(var[2]):
                        follower_queue.append(var[3])
                        q.out_queue.put(("PRIVMSG", "added " + var[2] + " to the queue"))
                    elif not var[2] == bot.channel:
                        nonfollower_queue.append(var[3])
                        q.out_queue.put(("PRIVMSG", "added " + var[2] + " to the queue"))
                    else:
                        follower_queue.insert(0, var[3])
                        q.out_queue.put(("PRIVMSG","YOU ARE SPECIAL " + var[3] + ", " + bot.channel + " has added you to the front of the line"))
                elif var[1] == "CLEAR":
                    follower_queue = []
                    nonfollower_queue = []
            elif var[0] == "GET USERSTATS":
                for i, viewer in enumerate(viewers):
                    if var[1] == viewer.name:
                        q.database_queue.put(("GET", "USERSTATS", viewer.name, viewer.join_time))
                        viewer.join_time = datetime.datetime.utcnow()
            elif var[0] == "VIEWER":
                if var[1] == "JOIN":
                    #hacky shit lol
                    if not viewers in var[2]:
                        viewers.append(var[2])
                        q.database_queue.put(("JOIN", var[2]))
                elif var[1] == "PART":
                    for i, viewer in enumerate(viewers):
                        if var[2].name == viewer.name:
                            q.database_queue.put(("PART", var[2]))
                            try:
                                viewers.pop(i)
                            except ValueError:
                                q.log_queue.put(("ERRORS", "viewer not removed: " + var[2].name + ", " + str(viewers)))
                            break
                elif var[1] == "UPDATE":
                    pass
            elif var[0] == "PERMIT":
                if var[1] == "+":
                    permits[var[2]] = 1
                if var[1] == "-":
                    try:
                        if permits[var[2]] == 1:
                            q.out_queue.put(("PRIVMSG", var[2] + " has used up their permit"))
                            permits[var[2]] = 0
                        else:
                            q.out_queue.put(("TIMEOUT", var[2]))
                            q.log_queue.put(("TIMEOUT", "Timed out user: " + var[2]))
                    except KeyError:
                        q.out_queue.put(("TIMEOUT", var[2]))
                        q.log_queue.put(("TIMEOUT", "Timed out user: " + var[2]))
            elif var[0] == "CV":
                if len(var) > 1:
                    if var[1] == "SET":
                        cv = var[2]
                        q.out_queue.put(("PRIVMSG", "Curse Voice set to: " + cv))
                else:
                    if cv:
                        q.out_queue.put(("PRIVMSG", "Curse Voice: " + str(cv)))
                    else:
                        q.out_queue.put(("PRIVMSG", "Curse Voice has not been set"))
            elif var[0] == "MODS":
                mods = var[1]
            elif var[0] == "FOLLOWERS":
                followers = var[1]
            elif var[0] == "HIGHLIGHT":
                import requests
                try:
                    vids = API.Twitch.get_channel_videos(bot.channel, False)
                    if len(vids["videos"]) > 0:
                        video = vids["videos"][0]["url"]
                except requests.exceptions.ConnectionError:
                    video = None
                if video:
                    q.out_queue.put(("PRIVMSG", video))
            elif var[0] == "PRINT":
                if var[1] == "followers":
                    q.out_queue.put(("PRIVMSG", str(followers)))
                    q.out_queue.put(("PRIVMSG", str(len(followers))))
                elif var[1] == "permits":
                    q.out_queue.put(("PRIVMSG", str(permits)))
                elif var[1] == "queues":
                    q.out_queue.put(("PRIVMSG", str(follower_queue) + ", " + str(nonfollower_queue)))
                elif var[1] == "users":
                    q.out_queue.put(("PRIVMSG", str(viewers)))
                elif var[1] == "mods":
                    q.out_queue.put(("PRIVMSG", str(mods)))
        else:
            sleep(1)
    print "sending final numbers..."
    for viewer in viewers:
        print viewer
        q.database_queue.put(("PART", viewer))
    q.database_queue.put(("KILL",))
    q.log_queue.put(("KILL",))
    print "VAR MANAGER"