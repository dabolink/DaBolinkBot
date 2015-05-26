import json
import requests

token = "DICTIONARY_API_TOKEN"
APIURL = "http://www.dictionaryapi.com/api/v1/references/"


def formatAPI(response):
    if response.status_code == 200:
        return json.loads(response.content.decode("utf-8"))
    print response.status_code
    print response.text
    return None

def get_definition(word):
    return formatAPI(requests.get(APIURL + "collegiate/xml/" + word + "?key=" + token))

if __name__ == "__main__":
    print get_definition("hello")