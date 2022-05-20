import requests


def getPhoto():
    response = requests.get(
        "https://api.unsplash.com/photos/random?client_id=mjxmWdfEkErf3EYA66iggKKsgywYcrsy5P7ABqJ5-hE"
    )
    return response.json()["urls"]["regular"]
