import requests


def bot_operation(channel, operation):
    header = {'Content-Type': 'application/json'}
    print requests.get("http://127.0.0.1:5000/dabolinkbot/api/v1.0/bot/{}/{}".format(operation, channel), headers=header).text


def get_channel_userstats(channel, user):
    header = {'Content-Type': 'application/json'}
    print requests.get("http://127.0.0.1:5000/dabolinkbot/api/v1.0/channel/{}/{}".format(channel, user), headers=header).text

def get_userstats(user):
    header = {'Content-Type': 'application/json'}
    print requests.get("http://127.0.0.1:5000/dabolinkbot/api/v1.0/user/{}".format(user), headers=header).text

if __name__ == "__main__":
    bot_operation("dabolink", "status")
    bot_operation("dabolink", "start")
    bot_operation("dabolink", "status")
    bot_operation("dabolink", "end")
    get_userstats("dabolink")
    get_channel_userstats("thepretenderr", "dabolink")