#has access/starts/ends all processes for each bot
import multiprocessing
from time import sleep
import datetime

import Objects.Bot
import Objects.Queues

import VariableManager.VarManager

import Irc.In
import Irc.Out
import Irc.CommandParser
import Irc.ChatModerator

import Logger.Logger

import Database.DatabaseUpdater

import Periodic.Followers
import Periodic.Check_Online

def startup(channel, check_online=False, q=None):
    if not q:
        q = Objects.Queues.queues()
    debug = False
    if debug:
        import sys
        sys.stderr = open('Logs/Errors/{}/Controller.txt'.format(channel), 'w')
    processes = []
    bot = Objects.Bot.Bot(channel, debug)
    processes.append(multiprocessing.Process(target=Irc.ChatModerator.start, args=(bot, q)))
    if check_online:
        processes.append(multiprocessing.Process(target=Periodic.Check_Online.start, args=(bot, q)))
        processes.append(multiprocessing.Process(target=Periodic.Followers.start, args=(bot, q)))
    processes.append(multiprocessing.Process(target=Logger.Logger.start, args=(bot, q)))
    processes.append(multiprocessing.Process(target=Database.DatabaseUpdater.start, args=(bot, q)))
    processes.append(multiprocessing.Process(target=Irc.In.start, args=(bot, q)))
    processes.append(multiprocessing.Process(target=Irc.Out.start, args=(bot, q)))
    processes.append(multiprocessing.Process(target=Irc.CommandParser.start, args=(bot, q)))
    processes.append(multiprocessing.Process(target=VariableManager.VarManager.start, args=(bot, q)))

    for process in processes:
        process.start()
    while q.kill_queue.empty():
        if not q.control_queue.empty():
            cmd = q.control_queue.get()
            if cmd[0] == "RESET":
                print "resetting"
                q.kill_queue.put("")
                for process in processes:
                    process.join()
                while not q.kill_queue.empty():
                    q.kill_queue.get()
                processes = []
                q = Objects.Queues.queues()
                processes.append(multiprocessing.Process(target=Periodic.Followers.main, args=(bot, q)))
                if check_online:
                    print "check online activated"
                    processes.append(multiprocessing.Process(target=Periodic.Check_Online.main, args=(bot, q)))
                processes.append(multiprocessing.Process(target=Periodic.LinesOfText.main, args=(bot, q)))
                processes.append(multiprocessing.Process(target=Logger.Logger.start, args=(bot, q)))
                processes.append(multiprocessing.Process(target=Database.DatabaseUpdater.start, args=(bot, q)))
                processes.append(multiprocessing.Process(target=Irc.In.start, args=(bot, q)))
                processes.append(multiprocessing.Process(target=Irc.Out.start, args=(bot, q)))
                processes.append(multiprocessing.Process(target=Irc.CommandParser.start, args=(bot, q)))
                processes.append(multiprocessing.Process(target=VariableManager.VarManager.start, args=(bot, q)))
                print "reset"
        else:
            sleep(bot.sleep_time*10)
    for process in processes:
        process.join()

if __name__ == "__main__":
    import sys
    startup(sys.argv[1])
