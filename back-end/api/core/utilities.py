import requests
import dns.resolver
from bs4 import BeautifulSoup
from django.core.mail import send_mail

WAPPALYZER_API_KEY = "y6zvx1SEJC5hx7rjnAvYu6jOqDEntYID91PGAlND"
UNSPLASH_API_KEY = "mjxmWdfEkErf3EYA66iggKKsgywYcrsy5P7ABqJ5-hE"
NVD_API_KEY = "09287fcf-8c39-4531-a50e-0a5132cb4664"


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
        count = 0
        for reference in references:
            if count < 5:
                ref_urls.append(reference["url"])
                count = count + 1

        description = cve["description"]["description_data"][0]["value"]
        cve_id = cve["CVE_data_meta"]["ID"]

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
                "cve_id": cve_id,
            }
        )
    return cves_array


def getCVEs(technology, version):
    if not version:
        version = "*"
    technology = technology.replace(" ", "_")
    technology = technology.replace("-", "_")
    cpeString1 = "cpe:2.3:a:*:" + technology + ":" + version + ":*:*:*:*:*:*:*"
    cpeString2 = "cpe:2.3:a:" + technology + ":*:" + version + ":*:*:*:*:*:*:*"

    cves = []

    endpoint1 = (
        "https://services.nvd.nist.gov/rest/json/cves/1.0/?cpeMatchString="
        + cpeString1
        + "&apiKey="
        + NVD_API_KEY
        + "&resultsPerPage=100"
    )
    endpoint2 = (
        "https://services.nvd.nist.gov/rest/json/cves/1.0/?cpeMatchString="
        + cpeString2
        + "&apiKey="
        + NVD_API_KEY
        + "&resultsPerPage=100"
    )

    response = requests.get(endpoint1)
    extraction = extractDataFromCVE(response)
    if extraction is not None:
        cves = cves + extraction

    """ response = requests.get(endpoint2)
    extraction = extractDataFromCVE(response)
    if extraction is not None:
        cves = cves + extraction """

    print("got cves for : " + technology + " : " + version)

    return cves


def getPhoto():
    response = requests.get(
        "https://api.unsplash.com/photos/random?orientation=squarish&content_filter=high&client_id="
        + UNSPLASH_API_KEY
    )
    return response.json()["urls"]["regular"]


def getTechs(url):
    if url.startswith("https://") == False:
        url = "https://" + url
    Headers = {"x-api-key": WAPPALYZER_API_KEY}
    endpoint = "https://api.wappalyzer.com/v2/lookup/?urls=" + url
    response = requests.get(endpoint, headers=Headers)
    print("Got Tech For : " + url)
    return response.json()


def verifyDomain(domainName, verifyCode):
    verificationText = "we-see-verification." + domainName + "=" + str(verifyCode)
    try:
        answers = dns.resolver.resolve(domainName, "TXT")
    except:
        return "Some Error Occurred"
    for rdata in answers:
        strData = str(rdata).strip('"')
        print("Verifying...")
        if verificationText == strData:
            return True
    return False


def findSubdomains(domainName):
    crtApi = "https://crt.sh/?Identity=" + domainName + "&exclude=expired&deduplicate=Y"
    response_html = requests.get(crtApi)
    soup = BeautifulSoup(response_html.content, features="html.parser")

    for e in soup.findAll("br"):
        e.extract()

    innerTable = soup.select("body > table")[1]
    tdArr = innerTable.select("tr > td:nth-child(6)")

    resArr = []

    for child in tdArr:
        for txt in child.contents:
            txt = txt.replace("www.", "")
            if txt not in resArr and txt != domainName:
                resArr.append(txt)

    return resArr


def sendCVEmail(data):
    print("sending mail...")
    subject = data["subject"]
    html_message = data["body"]
    plain_message = html_message.replace("<br/>", "\n")
    from_email = "news@weseecves.com"
    to = data["recepient"]

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
