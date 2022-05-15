import dns.resolver


def verifyDomain(domainName, verifyCode):
    verificationText = "we-see-verification." + domainName + "=" + str(verifyCode)
    try:
        answers = dns.resolver.resolve(domainName, "txt")
    except:
        return "Some Error Occurred"
    for rdata in answers:
        print(rdata)
        # if rdata == verificationText:
        #     return True
    return False
