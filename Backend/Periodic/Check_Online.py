from requests import ConnectionError
from time import sleep
import API.Twitch

def start(bot, q):
    if bot.debug:
        import sys
        sys.stderr = open('Logs/Errors/{}/Check_Online.txt'.format(bot.channel), 'w')
    i = 0
    sleep(60)
    while q.kill_queue.empty():
        try:
            stream = API.Twitch.get_stream(bot.channel)
            if not stream["stream"]:
                i += 1
                if i >= bot.offline_counter:
                    q.kill_queue.put("")
                print i
                sleep(2)
            else:
                i = 0
                sleep(30)
        except (TypeError, ConnectionError) as e:
            sleep(30)
            print "connection error > check online"
            q.log_queue.put(("ERROR", str(e) + " : some error occurred in check online"))
    print "CHECK ONLINE"
