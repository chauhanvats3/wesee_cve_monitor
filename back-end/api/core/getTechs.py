import requests


def getTechs(url):
    if url.startswith("https://") == False:
        url = "https://" + url
    print(url)
    Headers = {"x-api-key": "3wEhUN3jdo7cxfDX4w1US4Sh10aghQCm2YUcXOn9"}
    endpoint = "https://api.wappalyzer.com/v2/lookup/?urls=" + url
    response = requests.get(endpoint, headers=Headers)
    return response.json()
