import random
import time
from IPdomain import FormatIPDomain
from ip_tools.v4 import Mixed


def gen_random_ip():
    ip_section_1 = "220"
    ip_section_2 = random.choice(["180", "181", "182"])
    ip_section_3 = str(random.randrange(0, 254, 1))
    ip_section_4 = str(random.randrange(0, 254, 1))
    ip = ".".join([ip_section_1, ip_section_2, ip_section_3, ip_section_4])

    return ip

def gen_random_ips(n):
    ips = []
    for i in range(n):
        ip = gen_random_ip()
        ips.append(ip)
    return ips

def espp_check_ip(ipstring, iprange):
    ipcheck = FormatIPDomain(iprange)
    return ipstring in ipcheck

def espc_check_ip(ipstring, iprange):
    flag = False
    for ip_str in iprange:
        ipcheck = Mixed(ip_str)
        if ipcheck.include(ipstring):
            flag = True

    return flag


if __name__ == "__main__":
    iprange1 = ["220.180.*.*", "220.181.23-78.*", "220.181.50.*", "220.182.86-198.*"]
    iprange2 = ["220.180.0-255.0-255", "220.181.23-78.0-255", "220.181.50.0-255", "220.182.86-198.0-255"]

    for n in [1000, 10000, 100000, 1000000, 10000000]:
        print "num: %s" % n
        ips = gen_random_ips(n)
        i = 0; j = 0
        start_time = time.time()
        for ip in ips:
            flag = espp_check_ip(ip, iprange2)
            if flag:
                i += 1
        usedtime = time.time() - start_time
        print "espp", i, usedtime

        start_time = time.time()
        for ip in ips:
            flag = espc_check_ip(ip, iprange1)
            if flag:
                j += 1
        usedtime = time.time() - start_time
        print "espc", j, usedtime

