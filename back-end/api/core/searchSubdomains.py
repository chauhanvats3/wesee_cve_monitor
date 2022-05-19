import requests


def findSubdomains(domainName):
    subdomainApi = "https://dns.bufferover.run/dns?q=." + domainName
    response = requests.get(subdomainApi)
    return response.json()
