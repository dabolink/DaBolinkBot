from requests import ConnectionError
from time import sleep
from API.Twitch import *


def update_followers(q, num_followers, channel_follow):
    followers = []
    i = 0
    print num_followers
    while i < num_followers:
        followers.append(channel_follow["follows"][i]["user"]["name"])
        i += 1
    q.var_queue.put(("FOLLOWERS", followers))


def start(bot, q):
    if bot.debug:
        import sys
        sys.stderr = open('Logs/Errors/{}/Followers.txt'.format(bot.channel), 'w')
    try:
        channel_follow = get_channel_follows(bot.channel)
        num_followers = channel_follow["_total"]
        update_followers(q, num_followers, channel_follow)

        while q.kill_queue.empty():
            channel_follow = get_channel_follows(bot.channel)
            check_num = channel_follow["_total"]
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
                update_followers(q, num_followers, channel_follow)
                num_followers = check_num
            elif num_followers > check_num:
                print "lost follower"
                num_followers = check_num
                update_followers(q, num_followers, channel_follow)
            else:
                pass
            sleep(60)
    except ConnectionError:
        sleep(60)
        print "connection error > following"
    print "FOLLOWERS"
