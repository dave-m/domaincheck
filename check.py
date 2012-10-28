from dns import resolver, reversename


def get_a(domain_name):
    try: 
        answer = resolver.query(domain_name, 'A')
        return [a.address for a in answer]
    except (resolver.NoAnswer, resolver.NXDOMAIN):
        return []

def get_mx(domain_name):
    try:
        answer = resolver.query(domain_name, 'MX')
    except (resolver.NoAnswer, resolver.NXDOMAIN):
        return []
    return sorted(((str(a.exchange), a.preference) for a in answer), key=lambda x: x[1])

def get_ns(domain_name):
    try:
        answer = resolver.query(domain_name, 'NS')
        return [str(a.target) for a in answer]
    except (resolver.NoAnswer, resolver.NXDOMAIN):
        return []

def get_host(domain_name):
    # get IP
    a = get_a(domain_name)
    hosts = []
    for ip in a:
        reverse = str(reversename.from_address(str(ip)))
        name = resolver.query(reverse, 'PTR')
        hosts.append(name)

def full_search(domain_name):

    nameservers = get_ns(domain_name)
    mx = get_mx(domain_name)

    a_records = []
    for prefix in ['', 'www.', 'ftp.', 'mail.']:
        res = get_a(prefix+domain_name)
        if res:
            a_records.append( (prefix, res,) )

    return {"nameservers": nameservers,
            "mx": mx,
            "a": a_records}
