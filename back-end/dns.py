import dns.resolver

answers = dns.resolver.resolve("dnspython.org", "TXT")
for rdata in answers:
    print("Host", rdata.exchange, "has preference", rdata.preference)
