class FormatIPDomain(object):
    def __init__(self, ip_domain_list):
        self.ip_domain_list = ip_domain_list

    def __contains__(self, ip_str):
        seq = ip_str.split('.')
        if len(seq) != 4:
            return False
        for ip_domain in self.ip_domain_list:
            seq_domain = ip_domain.split('.')
            if len(seq_domain) != 4:
                return False
            if self.pattern(seq, seq_domain):
                # print 'pattern:', ip_domain
                # print ip_str
                return True
        return False

    def pattern(self, seq, seq_pattern):
        for i in range(4):
            if not self.inside(seq[i], seq_pattern[i]):
                return False
        return True

    def inside(self, ip_str, ip_pattern):
        try:
            ip_pattern_int = int(ip_pattern)
        except ValueError:
            ip_range = ip_pattern.split('-')
            return False if int(ip_str) < int(ip_range[0]) or int(ip_str) > int(ip_range[1]) else True
        return False if int(ip_str) != ip_pattern_int else True


if __name__ == '__main__':
    ip_domain = [
        '10.34-60.22.1',
        '10.33.2.1-100',
        '90.23.2-56.3-11',
        '10.0-255.0-255.0-255'
    ]
    a = FormatIPDomain(ip_domain)
    print '10.33.2.1' in a
