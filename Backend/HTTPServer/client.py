import requests


def start_bot(channel):
    header = {'Content-Type': 'application/json'}
    print requests.get("http://127.0.0.1:5000/dabolinkbot/api/v1.0/bot/{}/start".format(channel), headers=header).text


def get_channel_userstats(channel, user):
    header = {'Content-Type': 'application/json'}
    print requests.get("http://127.0.0.1:5000/dabolinkbot/api/v1.0/channel/{}/{}".format(channel, user), headers=header).text

def get_userstats(user):
    header = {'Content-Type': 'application/json'}
    print requests.get("http://127.0.0.1:5000/dabolinkbot/api/v1.0/user/{}".format(user), headers=header).text

if __name__ == "__main__":
    # print start_bot("dabolink")
    get_userstats("dabolink")
    get_channel_userstats("thepretenderr", "dabolink")