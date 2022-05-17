import requests


def findSubdomains(domainName):
    subdomainApi = "https://dns.bufferover.run/dns?q=." + domainName
    print(subdomainApi)
    response = requests.get(subdomainApi)
    return response.json()
