import requests
import vulners


""" def vulnerability(name, version):
    vulners_api = vulners.Vulners(
        api_key="XV07ZQ8AJ9FQ97M71NB0LM85SJSFKESBVFLRZ6VHOEAZ6UAHYAKY1KW1URN0DF3Q"
    )

    results = vulners_api.get_software_vulnerabilities(name, version)
    exploit_list = results.get("exploit")
    vulnerabilities_list = [
        results.get(key) for key in results if key not in ["info", "blog", "bugbounty"]
    ]
    print("Vulnersablities")
    print(vulnerabilities_list)
 """


def vulnerability(name, version):
    endpoint = "https://vulners.com/api/v3/burp/software/"
    headers = {"Content-Type: application/json"}
    print(name, version)
    if not version:
        version = ""
    queryData = {
        "software": name,
        "version": version,
        "type": "software",
        "maxVulnerabilities": 100,
        "apiKey": "XV07ZQ8AJ9FQ97M71NB0LM85SJSFKESBVFLRZ6VHOEAZ6UAHYAKY1KW1URN0DF3Q",
    }
    response = requests.post(endpoint, data=queryData, headers=headers)
    print(response)


def getCVEs(technology, version):
    apiKey = "09287fcf-8c39-4531-a50e-0a5132cb4664"
    cpeString1 = "cpe:2.3:a:*:" + technology + ":" + version + ":*:*:*:*:*:*:*"
    cpeString1 = "cpe:2.3:a:" + technology + ":*:" + version + ":*:*:*:*:*:*:*"

    endpoint = "https://services.nvd.nist.gov/rest/json/cves/1.0/?keyword=" + technology
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
    Headers = {"x-api-key": "wTTICpi0as1Hve1F2JjuG8qtAN361yFsavAsUSlQ"}
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
