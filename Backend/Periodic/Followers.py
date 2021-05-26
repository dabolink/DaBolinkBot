from requests import ConnectionError
from time import sleep
from API.Twitch import *


def update_followers(channel, q):
    followers = []
    offset = 0
    limit = 100
    channel_follow = get_channel_follows(channel, limit, offset)
    num_followers = channel_follow["_total"]
    i = 0
    while i < num_followers:
        try:
            if i >= offset + limit:
                offset += limit
                channel_follow = get_channel_follows(channel, limit, offset)
            followers.append(channel_follow["follows"][i - offset]["user"]["name"])
            i += 1
        except IndexError:
            print "INDEX ERROR: ", i, offset, limit
            offset += limit
    print followers[0], followers[len(followers) - 1]
    q.log_queue.put(("FOLLOWERS", str(followers)))
    q.var_queue.put(("FOLLOWERS", followers))


def start(bot, q):
    j = 0.0
    print bot.periodic_sleep
    if bot.debug:
        import sys
        sys.stderr = open('Logs/Errors/{}/Followers.txt'.format(bot.channel), 'w')
    try:
        channel_follow = get_channel_follows(bot.channel, q)
    except ConnectionError:
        sleep(60)
        print "connection error > following"
        channel_follow["_total"] = 0
    num_followers = channel_follow["_total"]
    update_followers(bot.channel, q)
    sleep(bot.periodic_sleep)
    while q.kill_queue.empty():
        try:
            channel_follow = get_channel_follows(bot.channel, q)
            check_num = channel_follow["_total"]
        except ConnectionError:
            sleep(bot.periodic_sleep)
            print "connection error > following"
            continue
        if num_followers < check_num:
            print "new follower"
            follow_str = ""
            difference = check_num - num_followers
            i = 0
            while i < difference:
                follow_str += channel_follow["follows"][i]["user"]["name"] + ", "
                i += 1
            follow_str = "new follower!!!! {} !!!! RAISE YOUR KAPPAS Kappa Kappa Kappa Kappa !!!!".format(follow_str[:-2])
            q.out_queue.put(("PRIVMSG", follow_str))
            update_followers(bot.channel, q)
            num_followers = check_num
        elif num_followers > check_num:
            print "lost follower"
            num_followers = check_num
            update_followers(bot.channel, q)
        else:
            incr = bot.periodic_sleep / float(60)
            print incr
            j += incr
            if j >= 5:
                j = 0
                q.out_queue.put(("MESSAGE",))
            print "no new followers", num_followers, j
        sleep(bot.periodic_sleep)
    print "FOLLOWERS"
