import requests
import time


def extractDataFromCVE(response):
    cves_array = []
    try:
        results = response.json()["result"]["CVE_Items"]
    except:
        return None

    for item in results:
        ref_urls = []
        cve = item["cve"]
        references = cve["references"]["reference_data"]
        for reference in references:
            ref_urls.append(reference["url"])
        description = cve["description"]["description_data"][0]["value"]
        score = None
        severity = None
        try:
            score = item["impact"]["baseMetricV3"]["cvssV3"]["baseScore"]
            severity = item["impact"]["baseMetricV3"]["cvssV3"]["baseSeverity"]
        except:
            score = item["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]
            severity = item["impact"]["baseMetricV2"]["severity"]

        cves_array.append(
            {
                "references": ref_urls,
                "description": description,
                "severity": severity,
                "score": score,
            }
        )
    return cves_array


def getCVEs(technology, version):
    print("Getting CVEs for : " + technology + " : " + version)
    if not version:
        version = "*"
    technology = technology.replace(" ", "_")
    technology = technology.replace("-", "_")
    apiKey = "09287fcf-8c39-4531-a50e-0a5132cb4664"
    cpeString1 = "cpe:2.3:a:*:" + technology + ":" + version + ":*:*:*:*:*:*:*"
    cpeString2 = "cpe:2.3:a:" + technology + ":*:" + version + ":*:*:*:*:*:*:*"

    cves = []

    endpoint1 = (
        "https://services.nvd.nist.gov/rest/json/cves/1.0/?cpeMatchString="
        + cpeString1
        + "&apiKey="
        + apiKey
        + "&resultsPerPage=200"
    )
    endpoint2 = (
        "https://services.nvd.nist.gov/rest/json/cves/1.0/?cpeMatchString="
        + cpeString2
        + "&apiKey="
        + apiKey
        + "&resultsPerPage=200"
    )

    response = requests.get(endpoint1)
    extraction = extractDataFromCVE(response)
    if extraction is not None:
        cves = cves + extraction

    response = requests.get(endpoint2)
    extraction = extractDataFromCVE(response)
    if extraction is not None:
        cves = cves + extraction

    print("got cves for : " + technology)

    return cves


def getPhoto():
    response = requests.get(
        "https://api.unsplash.com/photos/random?orientation=squarish&content_filter=high&client_id=mjxmWdfEkErf3EYA66iggKKsgywYcrsy5P7ABqJ5-hE"
    )
    return response.json()["urls"]["regular"]


def getTechs(url):
    print("Getting Tech For : " + url)
    if url.startswith("https://") == False:
        url = "https://" + url
    Headers = {"x-api-key": "ckC7d24CNN8MWObSSmZri2vtGrpb9cfP7R8eCdDn"}
    endpoint = "https://api.wappalyzer.com/v2/lookup/?urls=" + url
    response = requests.get(endpoint, headers=Headers)
    print("Got Tech For : " + url)
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
    print("Finding Subdomains : " + domainName)
    subdomainApi = "https://dns.bufferover.run/dns?q=." + domainName
    response = requests.get(subdomainApi)
    print("Got subdomains for : " + domainName)
    return response.json()
