from dns import resolver, reversename
import socket

WHOIS_SERVER = 'whois.ripe.net'

def whois(domain_name):
    """Run a quick whois for a domain name

    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.connect((domain_name.split('.')[-1]+'.whois-servers.net', 43))
        soc.send(domain_name+'\r\n')
    except:
        return ''

    response = ''
    while True:
        res_chunk = soc.recv(4096)
        response += res_chunk
        if not res_chunk:
            break

    soc.close()

    return response

def get_a(domain_name):
    """Get the A records, return list of addresses

    """
    try:
        answer = resolver.query(domain_name, 'A')
        return [a.address for a in answer]
    except (resolver.NoAnswer, resolver.NXDOMAIN):
        return []

def get_mx(domain_name):
    """Get MX records, return list of tuples of (record, preference)

    """
    try:
        answer = resolver.query(domain_name, 'MX')
    except (resolver.NoAnswer, resolver.NXDOMAIN):
        return []

    return sorted(
            ((str(a.exchange), a.preference) for a in answer),
            key=lambda x: x[1])

def get_ns(domain_name):
    """Get the NS (nameserver) records, return list of IP addresses

    """
    try:
        answer = resolver.query(domain_name, 'NS')
        return [str(a.target) for a in answer]
    except (resolver.NoAnswer, resolver.NXDOMAIN):
        return []

def full_search(domain_name):
    """Get the A, MX, Nameservers and whois records
    for the supplied domain name

    Check ``www``, ``ftp``, ``mail``, and naked domain A records

    """

    nameservers = get_ns(domain_name)
    a_records = []
    for prefix in ['', 'www.', 'ftp.', 'mail.']:
        res = get_a(prefix+domain_name)
        if res:
            a_records.append( (prefix, res,) )

    whois_results = whois(domain_name)

    return {"nameservers": nameservers,
            "mx": get_mx(domain_name) ,
            "a": a_records,
            "whois": whois_results}

