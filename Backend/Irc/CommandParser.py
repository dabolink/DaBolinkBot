from time import sleep


def admin_commands(bot, q, user, command, parameters=None):
    if user == "dabolink" or user == bot.channel:
        if command == "time":
            if parameters[0] == "add":
                # Database.add_time(parameters[1], int(parameters[2]))
                pass
            #TODO reimplement
    if command == "next":
        q.var_queue.put(("QUEUE", "GET"))
    elif command == "quote":
        if parameters:
            if parameters[0] == "add":

                #TODO reimplement
                # Database.add_quote(Variables.Channel, " ".join(parameters[1:]))
                # IRC.irc_send("added quote to db")
                pass
        else:
            # try:
            #     quote = Database.get_random_quote(Variables.Channel)
            #     IRC.irc_send("\"" + quote[1] + "\"" + " - " + quote[2] + "(" + quote[0] + ")")
            # except IndexError:
            #     print "no quotes"
            pass
    elif command == "toggle":
        if parameters[0] == "links" and len(parameters) == 1:
            q.out_queue.put(("TOGGLE",))
        elif parameters[0] == "links":
            if parameters[1] == "off":
                q.out_queue.put(("TOGGLE", "OFF"))
            elif parameters[1] == "on":
                q.out.queue.put(("TOGGLE", "ON"))

    elif command == "bookmark":
        q.log_queue.put(("BOOKMARK",))
        q.out_queue.put(("PRIVMSG", "bookmark logged"))
    elif command == "cv":
        if parameters:
            if parameters[0] == "set":
                q.var_queue.put(("CV", "SET", parameters[1]))
        else:
            commands(bot, q, user, "cv", parameters)
        pass

    elif command == "permit":
        q.var_queue.put(("PERMIT", "+", parameters[0]))
        q.out_queue.put(("PRIVMSG", "{} permits {} to post ONE(1) link".format(user, parameters[0])))

    elif command == "execute":
        q.kill_queue.put("")

    elif command == "test":
        pass

    elif command == "clear":
        q.var_queue.put(("QUEUE", "CLEAR"))
        q.out_queue.put(("PRIVMSG", "Queue has been cleared"))
        pass

    elif command == "print":
        if parameters:
            q.var_queue.put(("PRINT", parameters[0]))

    elif command == "reset":
        pass
        # q.control_queue.put(("RESET",))

    elif command == "users":
        q.var_queue.put(("PRINT", command))
        pass
    else:
        commands(bot, q, user, command, parameters)


def commands(bot, q, user, command, parameters):
    if command == "topstats":
        if not parameters:
            q.database_queue.put(("GET", "TOPSTATS"))

    if command == "userstats":
        if not parameters:
            q.var_queue.put(("GET USERSTATS", user))
        else:
            q.var_queue.put(("GET USERSTATS", " ".join(parameters)))
    elif command == "cv":
        q.var_queue.put(("CV",))
    elif command == "dabolinkbot":
        q.out_queue.put(("PRIVMSG", "DaBolinkbot is superior to non-bots"))
    elif command == "uptime":
        import Time.Time
        Time.Time.uptime(bot, q)
        pass
    elif command == "highlight":
        q.var_queue.put(("HIGHLIGHT",))
    elif command == "add":
        if not parameters:
            q.out_queue.put(("PRIVMSG", "type '!add <ign>' to be added to the queue"))
        else:
            u = " ".join(parameters)
            q.var_queue.put(("QUEUE", "PUT", user, u))
    else:
        pass


def start(bot, q):
    if bot.debug:
        import sys
        sys.stderr = open('Logs/Errors/{}/CommandParser.txt'.format(bot.channel), 'w')
    while q.kill_queue.empty():
        if not q.command_queue.empty():
            cmd = q.command_queue.get()
            #(T/F,  (command, params))
            if cmd[0].admin:
                admin_commands(bot, q, cmd[0].name, cmd[1][0][1:], cmd[1][1:])
            else:
                commands(bot, q, cmd[0].name, cmd[1][0][1:], cmd[1][1:])
        else:
            sleep(1)
    print "COMMAND PARSER"