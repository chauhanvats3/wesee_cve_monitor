import requests


def getTechs(url):
    if url.startswith("https://") == False:
        url = "https://" + url
    Headers = {"x-api-key": "rguTeBO1wS9vEf34gMjey1oHjq5pDd6Sdtt0iuV4"}
    endpoint = "https://api.wappalyzer.com/v2/lookup/?urls=" + url
    response = requests.get(endpoint, headers=Headers)
    return response.json()
