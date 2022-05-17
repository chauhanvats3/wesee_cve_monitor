import dns.resolver


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
