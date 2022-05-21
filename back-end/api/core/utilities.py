import requests


def getCVEs(technology):
    apiKey = "09287fcf-8c39-4531-a50e-0a5132cb4664"
    endpoint = (
        "https://services.nvd.nist.gov/rest/json/cves/1.0/?keyword="
        + technology
        + "?apiKey="
        + apiKey
        + "?isExactMatch=true"
    )
    response = requests.get(endpoint)
    return response.json()


def getPhoto():
    response = requests.get(
        "https://api.unsplash.com/photos/random?client_id=mjxmWdfEkErf3EYA66iggKKsgywYcrsy5P7ABqJ5-hE"
    )
    return response.json()["urls"]["regular"]


def getTechs(url):
    if url.startswith("https://") == False:
        url = "https://" + url
    Headers = {"x-api-key": "yJ5voPaXwZ5un1OExGwiJ3ruA6clQ7am6rJoAUoW"}
    endpoint = "https://api.wappalyzer.com/v2/lookup/?urls=" + url
    response = requests.get(endpoint, headers=Headers)
    return response.json()


def verifyDomain(domainName, verifyCode):
    verificationText = "we-see-verification." + domainName + "=" + str(verifyCode)
    try:
        answers = dns.resolver.resolve(domainName, "txt")
    except:
        return "Some Error Occurred"
    for rdata in answers:
        strData = str(rdata).strip('"')
        if verificationText == strData:
            return True
    return False


def findSubdomains(domainName):
    subdomainApi = "https://dns.bufferover.run/dns?q=." + domainName
    response = requests.get(subdomainApi)
    return response.json()
