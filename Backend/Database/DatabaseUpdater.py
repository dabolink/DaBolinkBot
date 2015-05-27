import datetime
import math
import time
import sqlite3


def incrementLOTS(LOT):
    global cur, conn
    for user in LOT:
        cur.execute("UPDATE Users SET lines_of_text = lines_of_text + ? WHERE user = ?", (LOT[user], user))
    conn.commit()


def getUser(user):
    global cur, conn
    return cur.execute("SELECT * from Users WHERE User = ?", (user,)).fetchone()


def addUser(user):
    global cur, conn
    print "adding user", user
    cur.execute("INSERT INTO Users VALUES (?, ?, ?, ?)", (user, 0, 0, 0))
    conn.commit()

def addTime(user, time):
    cur.execute("UPDATE Users SET hours = hours + ? WHERE user = ?", (time, user))
    conn.commit()

def start(bot, q):
    killSecure = False
    LOT = {}
    global cur
    global conn
    conn = sqlite3.connect("Database/Databases/{}.db".format(bot.channel))
    cur = conn.cursor()
    if bot.debug:
        import sys
        sys.stderr = open('Logs/Errors/{}/DatabaseUpdater.txt'.format(bot.channel), 'w')
    #create tables
    cur.execute("create table if not exists Users (user text, hours real, credits real, lines_of_text int, PRIMARY KEY(user))")
    cur.execute("create table if not exists Quotes (date text, quote text, channel text)")
    cur.execute("create table if not exists Channels (timeout  integer, follow_string text, curse_voice text)")
    conn.commit()

    while q.kill_queue.empty() or not killSecure:
        if not q.database_queue.empty():
            cmd = q.database_queue.get()
            if cmd[0] == "JOIN":
                user = cur.execute("SELECT * from Users WHERE User = ?",(cmd[1].name,)).fetchone()
                if not user:
                    q.log_queue.put(("DATABASE", "added {} to database".format(cmd[1].name)))
                    addUser(cmd[1].name)
                    print "{} added to database".format(cmd[1].name)
                else:
                    q.log_queue.put(("DATABASE", "{} has joined the channel".format(cmd[1].name)))
            elif cmd[0] == "GET":
                if cmd[1] == "USERSTATS":
                    total_time = datetime.datetime.utcnow() - cmd[3]
                    seconds = total_time.total_seconds()
                    t = seconds / 3600
                    addTime(cmd[2], t)
                    user = getUser(cmd[2])
                    if user:
                        hours = math.floor(user[1])
                        minutes = math.floor((user[1] - hours) * 60)
                        q.out_queue.put(("PRIVMSG", "{} has been in chat for {} hour(s) and {} minute(s) and has written {} line(s) of text".format(user[0], str(int(hours)), str(int(minutes)), str(user[3]))))
                        q.log_queue.put(("DATABASE", "got userstats for {} : {}".format(cmd[2], str(user))))
                    else:
                        q.out_queue.put(("PRIVMSG", "{}, there has been an error im srry :(".format(user[0])))
                        q.log_queue.put(("DATABASE", "error getting {} from database".format(user[0])))
                if cmd[1] == "TOPSTATS":
                    top_users = cur.execute("SELECT * from Users ORDER BY hours DESC").fetchall()
                    i = 1
                    outString = ""
                    for user in top_users:
                        outString += user[0] + "{} : {} hours, {} lines of text".format(str(int(user[1])), str(user[3]))
                        if i >= 10:
                            break
                        i += 1
                    q.out_queue.put(("PRIVMSG", outString))
                    q.log_queue.put(("DATABASE", "top users requested"))
            elif cmd[0] == "PART":
                total_time = datetime.datetime.utcnow() - cmd[1].join_time
                seconds = total_time.total_seconds()
                t = seconds / 3600
                addTime(cmd[1].name, t)
                q.log_queue.put(("DATABASE", "{} left the channel".format(cmd[1].name)))
            elif cmd[0] == "KILL":
                killSecure = True

            elif cmd[0] == "incLOT":
                try:
                    LOT[cmd[1]] += 1
                except KeyError:
                    LOT[cmd[1]] = 1
        else:
            if not LOT == {}:
                incrementLOTS(LOT)
                LOT = {}
            time.sleep(1)
    print "DATABASE UPDATER"
