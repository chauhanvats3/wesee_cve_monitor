import dns.resolver


def verifyDomain(domainName, verifyCode):
    verificationText = "we-see-verification." + domainName + "=" + verifyCode
    try:
        answers = dns.resolver.resolve(domainName, "TXT")
    except:
        return "Some Error Occurred"
    for rdata in answers:
        if rdata == verificationText:
            return True
    return False
