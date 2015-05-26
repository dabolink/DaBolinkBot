import datetime
import API.Twitch


def time_to_datetime(time):
    return datetime.datetime(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec)


def getTimeDiff(start_time, cur_time):
    from time import strptime
    s_time = strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
    dt_cur_time = time_to_datetime(cur_time)
    dt_s_time = time_to_datetime(s_time)
    return dt_cur_time - dt_s_time


def getUpTime(start_time, cur_time):
    # 2015-04-18T19:53:28Z
    diff = getTimeDiff(start_time, cur_time)
    date_str = ""
    if diff.days > 0:
        date_str += str(diff.days) + " day"
        if diff.days > 1:
            date_str += "s"
        date_str += ", "
    total_seconds = diff.total_seconds()
    hours = total_seconds / 3600
    total_seconds %= 3600
    minutes = total_seconds / 60
    total_seconds %= 60
    seconds = total_seconds
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    if hours > 0:
        date_str += str(hours) + " hour"
        if hours > 1:
            date_str += "s"
        date_str += ", "
    if minutes > 0:
        date_str += str(minutes) + " minute"
        if minutes > 1:
            date_str += "s"
    if diff.total_seconds() >= 60 or diff.days < 0:
        date_str += ", "
        date_str += "and "
    date_str += str(seconds) + " second"
    if seconds > 1:
        date_str += "s"
    return date_str

def uptime(bot, q):
    stream = API.Twitch.get_stream(bot.channel)["stream"]
    if stream:
        from time import gmtime
        curTime = gmtime()
        uptime = getUpTime(stream["created_at"], curTime)
        q.out_queue.put(("PRIVMSG", "Stream has been up for: " + uptime))
    else:
        q.out_queue.put(("PRIVMSG", "stream is not up"))