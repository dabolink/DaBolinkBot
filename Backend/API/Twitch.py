import json
import requests

ClientID = "CLIENT_ID"
redirect = "http://localhost"
token = "OAUTH_TOKEN"
APIURL = "https://api.twitch.tv/kraken/"


def formatAPI(response):
    if response.status_code == 200:
        return json.loads(response.content.decode("utf-8"))
    return None

def get_stream(user):
    return formatAPI(requests.get(APIURL + "/streams/{}".format(user)))

#Channel-v2.0
def get_channel(user):
    """
    retrieve channel info
    [updated_at, video_banner, logo, partner, display_name, delay, followers, _links, broadcaster_language, status,
        views, game, background, banner, name, language, url, created_at, mature, profile_banner_background_color, _id,
            profile_banner]
    """
    return formatAPI(requests.get(
        APIURL + "/channels/{}".format(user)))


def get_channel_follows(user, limit=100, offset=0):
    return formatAPI(requests.get(
        APIURL + "/channels/{}/follows?limit={}&offset={}".format(user, str(limit), offset)))


def put_channel_status(status):
    return formatAPI(requests.get('https://api.twitch.tv/kraken/channels/dabolink?channel[status]='+status+'&Autorization=' +token+'&_method=put'))


def get_channel_videos(user, broadcasts):
    if broadcasts:
        return formatAPI(requests.get(APIURL + "/channels/{}/videos?broadcasts=True".format(user)))
    else:
        return formatAPI(requests.get(APIURL + "/channels/{}/videos".format(user)))


def get_channel_viewers(user):
    # https://tmi.twitch.tv/group/user/thepretenderr/chatters
    """

    :param user:
    :return:
    """
    return formatAPI(requests.get("http://tmi.twitch.tv/group/user/{}/chatters".format(user)))

def get_subscribers(channel):
    return formatAPI(requests.get(APIURL + "channels/{}/subscriptions".format(channel)))


def get_most_recent_highlight(user):
    vids = get_channel_videos(user, False)
    if len(vids["videos"]) > 0:
        return vids["videos"][0]["url"]

if __name__ == "__main__":
    print get_channel_viewers("thepretenderr")
    print get_subscribers("thepretenderr")
