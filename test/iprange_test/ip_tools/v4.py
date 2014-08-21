#!/usr/bin/env python
# --coding:Utf-8
import os
import sys
import time
import re
import ctypes 
import logging

from v4_utils import *
from v import IPBase

def validate_ip(ip_str):
    sep = ip_str.split('.')
    if len(sep) != 4:
        return False
    for i,x in enumerate(sep):
        try:
            int_x = int(x)
            if int_x < 0 or int_x > 255:
                return False
        except ValueError, e:
            return False
    return True

class FromatError(Exception):
    '''format error code'''
    def __init__(self, ipstr):
        self.ipstr = ipstr
        super(FromatError, self).__init__()
    def __str__(self):
        errror_str = 'Wrong IP Format: %s' % self.ipstr
        return repr(errror_str)

class Single(IPBase):
    '''192.168.1.1'''
    def __init__(self, ipstring):
        self.ipstring = ipstring
        start = self.get_min(True)
        end = self.get_max(True)
        count = end - start + 1
        super(Single, self).__init__(ipstring, start, end, count)

    def get_min(self, rtnum=False):
        rt_min = self.ipstring
        if rtnum:
            return ip2long(rt_min)
        return rt_min

    def get_max(self, rtnum=False):
        rt_max = self.ipstring
        if rtnum:
            return ip2long(rt_max)
        return rt_max

    @classmethod
    def validate(cls, ipstring):
        return validate_ip(ipstring)

class CIDR(IPBase):
    '''192.168.1.1/8'''
    def __init__(self, ipstring):
        self.separate = ipstring.split('/')
        start = self.get_min(True)
        end = self.get_max(True)
        count = end - start + 1
        super(CIDR, self).__init__(ipstring, start, end, count)

    def get_min(self, rtnum=False):
        rt_min = get_network(self.separate[0], self.separate[1])
        if rtnum:
            return rt_min
        return long2ipv4(rt_min)

    def get_max(self, rtnum=False):
        rt_max = get_boardcast(self.separate[0], self.separate[1])
        if rtnum:
            return rt_max
        return long2ipv4(rt_max)

    @classmethod
    def validate(cls, ipstring):
        sep_cidr = ipstring.split('/')
        if len(sep_cidr) != 2:
            return False
        try:
            cidr = int(sep_cidr[1])
            if cidr < 0 or cidr > 32:
                return False
        except ValueError,e:
            return False
        return validate_ip(sep_cidr[0])


class Glob(IPBase):
    '''
        192.168.1.*
        192.168.*.*
        192.*.*.*
        *.*.*.*
    '''
    def __init__(self, ipstring):
        self.ipstring = ipstring
        start = self.get_min(True)
        end = self.get_max(True)
        count = end - start + 1
        super(Glob, self).__init__(ipstring, start, end, count)
    
    def get_min(self, rtnum=False):
        rt_min = self.ipstring.replace('*','0')
        if rtnum:
            return ip2long(rt_min)
        return rt_min
    
    def get_max(self, rtnum=False):
        rt_max = self.ipstring.replace('*','255')
        if rtnum:
            return ip2long(rt_max)
        return rt_max

    @classmethod
    def validate(cls, ipstring):
        sep = ipstring.split('.')
        if len(sep) is not 4:
            return False
        pat = ['*.*.*.*','.*.*.*', '.*.*', '.*']
        pat_id = None
        for x in range(4):
            if ipstring.endswith(pat[x]):
                pat_id = x
                break
        if pat_id is None:
            return False
        for i,x in enumerate(sep[:pat_id]):
            try:
                int_x = int(x)
                if int_x < 0 or int_x > 255:
                    return False
            except ValueError,e:
                return False
        return True


class Xrange(IPBase):
    '''192.168.1.1-10'''
    def __init__(self, ipstring):
        self.separate = re.split('[.-]', ipstring)
        start = self.get_min(True)
        end = self.get_max(True)
        count = end - start + 1
        super(Xrange, self).__init__(ipstring, start, end, count)

    def get_min(self, rtnum=False):
        rt_min = '.'.join(self.separate[:-1])
        if rtnum:
            return ip2long(rt_min)
        return rt_min

    def get_max(self, rtnum=False):
        rt_max = '.'.join(self.separate[:-2] + self.separate[-1:])
        if rtnum:
            return ip2long(rt_max)
        return rt_max
    
    def get_next(self, n=1):
        if n is 1 :
            if self.index < self.count:
                self.index += 1
            else :
                self.index = 0
                return None
        else :
            if n <= 0 or n > self.count:
                return None
            self.index = n
        ip_sep = self.separate[:-2] + [str(int(self.separate[-2])+self.index-1)]
        return '.'.join(ip_sep)

    @classmethod
    def validate(cls, ipstring):
        sep_cidr = ipstring.split('-')
        if len(sep_cidr) is not 2:
            return False
        try:
            cidr = int(sep_cidr[1])
            if cidr < 0 or cidr > 255:
                return False
        except ValueError,e:
            return False
        return validate_ip(sep_cidr[0])


class Mixed(IPBase):
    '''
        192.168.1-10.*
        192-195.*.*.*
        192.168-170.*.*
    '''
    def __init__(self, ipstring):
        self.separate = re.split('[.-]', ipstring)
        self.cnt = ipstring.count('*')
        start = self.get_min(True)
        end = self.get_max(True)
        count = end - start + 1
        super(Mixed, self).__init__(ipstring, start, end, count)
        
    def get_min(self, rtnum=False):
        prefix = '.'.join(self.separate[:4-self.cnt])
        suffix = '.'.join('0'*self.cnt)
        rt_min = '%s.%s' % (prefix, suffix)
        if rtnum :
            return ip2long(rt_min)
        return rt_min
    
    def get_max(self, rtnum=False):
        prefix = '.'.join(self.separate[:4-self.cnt-1]+ [self.separate[-self.cnt-1]])
        suffix = '.'.join(['255']*self.cnt)
        rt_max = '%s.%s' % (prefix, suffix)
        if rtnum :
            return ip2long(rt_max)
        return rt_max

    @classmethod
    def validate(cls, ipstring):
        sep = ipstring.split('.')
        if len(sep) is not 4:
            return False
        pat = ['.*.*.*', '.*.*', '.*']
        pat_id = None
        for x in range(3):
            if ipstring.endswith(pat[x]):
                pat_id = x
                break
        if pat_id is None:
            return False
        if sep[pat_id].count('-') != 1:
            return False
        pre_sep = sep[:pat_id] + sep[pat_id].split('-')
        for i,x in enumerate(pre_sep):
            try:
                int_x = int(x)
                if int_x < 0 or int_x > 255:
                    return False
            except ValueError,e:
                return False
        return True


class IPAddress():
    '''all maxied string'''
    def __init__(self , raw_string):
        self.sep = ','
        self.contain = []
        self.ip_format = [Single, CIDR, Glob, Xrange, Mixed]
        self.raw_string = raw_string
        self.validate()
        self.a = 10

    def validate(self):
        self.section = self.raw_string.split(self.sep)
        for x in self.section:
            valid = False
            for v in self.ip_format:
                if v.validate(x):
                    valid = True
                    self.contain.append([x, v(x)])
                    break
            if not valid:
                raise FromatError,x
        return True

    def get_list(self):
        rt_ip = set()
        for obj in self.contain:
            ip = obj[1].get_next()
            while ip is not None:
                rt_ip.add(ip)
                ip = obj[1].get_next()
        return rt_ip

    def get_range(self):
        rt_range = []
        for obj in self.contain:
            start = obj[1].get_min(rtnum=True)
            end = obj[1].get_max(rtnum=True)
            rt_range.append([start, end])
        return rt_range

    def __sub__(self, obj):
        collect_a = combine(self.get_range())
        collect_b = combine(obj.get_range())
        for b in collect_b:
            rt_list = []
            for a in collect_a:
                rt = get_difference(a, b)
                if rt is not None:
                    rt_list.extend(rt)
            if len(rt_list) == 0:
                return None
            collect_a = rt_list
        return collect_a


def ipv42long(ipstring):
    nums = [int(x) for x in ipstring.split('.')]
    return (nums[0]<<24) + (nums[1]<<16) + (nums[2]<<8) + nums[3]

def long2ipv4(integer):
    octets = []
    for i in range(4):
        octets.insert(0, str(integer & 0xFF))
        integer >>= 8
    return '.'.join(octets)

        
def validatelpRangeFormat(ipRange):
    '''usage : check the IP format.'''
    ip_format = [Single, CIDR, Glob, Xrange, Mixed]
    section = ipRange.split(',')
    for x in section:
        valid = False
        for v in ip_format:
            if v.validate(x):
                valid = True
                break
        if not valid:
            return False
    return True

def getIPList(ipRange):
    '''usage : get all IP.'''
    try:
        ipaddress = IPAddress(ipRange)
        rt_lsit = ipaddress.get_list()
        return list(rt_lsit)
    except FromatError,e:
        logging.error(str(e))
        return []

def getIPRangeBoundList(ipRange, combined=False, rtNum=False):
    '''usage : to obtain a list IP range.
       input : ipRange:'1.1.1.*,2.2.2.*'
       output: [['2.2.2.0', '2.2.2.255'], ['1.1.1.0', '1.1.1.255']]
    '''
    try:
        ipaddress = IPAddress(ipRange)
        r_list = ipaddress.get_range()
        if combined:
            r_list = combine(r_list)
        if rtNum:
            return r_list
        for i in range(len(r_list)):
            r_list[i][0] = long2ipv4(r_list[i][0])
            r_list[i][1] = long2ipv4(r_list[i][1])
        return  r_list 
    except FromatError,e:
        logging.error(str(e))
        return []

def _join_ip(start_str, end_str):
    rt_list = []
    sec_a = start_str.split('.')
    sec_b = end_str.split('.')
    for i in range(4):
        if sec_a[i] == sec_b[i]:
            rt_list.append(sec_a[i])
        else:
            rt_list.append(sec_a[i]+'-'+sec_b[i])
    ip = '.'.join(rt_list)
    ip = ip.replace('.0-255','.*')
    return ip

def rangeFormat(range_list):
    '''usage : mergage to supported formats.
       input : '1.1.1.1,1.1.1.2,1.1.5.*,1.1.6.*'
       output: [['1.1.1.1-2'], ['1.1.5-6.*']]
    '''
    try:
        result = []
        ipad = IPAddress(range_list)
        r_list = ipad.get_range()
        r_list = combine(r_list)
        for x in r_list:
            ip_list = [_join_ip(var[0], var[1]) for var in range2IP(x[0], x[1])]
            result.extend(ip_list)
        return result
    except FromatError,e:
        logging.error(str(e))
        return []

def getDifferenceIRange(range_a, range_list_b):
    '''usage : obtain difference set and format to
               to a specified format.
       input : range_a: '1.1.1-3.*'
               range_list_b: ['1.1.1.*','1.1.1-2.*']
       output: ['1.1.3.*']
    '''
    try:
        ipad_a = IPAddress(range_a)
        ipad_b = IPAddress(','.join(range_list_b))
        diff = ipad_a - ipad_b
        if diff is None:
            return []
        diff = combine(diff)
        result = []
        for x in diff:
            ip_list = [_join_ip(var[0], var[1]) for var in range2IP(x[0], x[1])]
            result.extend(ip_list)
        return result
    except FromatError,e:
        logging.error(str(e))
        return []


def getRestRange(ipList):
    '''usage : get the opposite collection.
       input : '1.0-255.*.*'
       output: ['2-254.*.*.*']
    '''
    #1.0.0.0.0 - 254.255.255.255
    try:
        total = [[ip2long('1.0.0.0'), ip2long('254.255.255.255')]]
        obj = IPAddress(ipList)
        ip_range = combine(obj.get_range())
        for var1 in ip_range:
            temp_diff = []
            for var2 in total:
                diff = get_difference(var2, var1)
                if diff is not None:
                    temp_diff.extend(diff)
            if len(temp_diff) == 0:
                return []
            total = temp_diff
        result = []
        for x in total:
            ip_list = [_join_ip(var[0], var[1]) for var in range2IP(x[0], x[1])]
            result.extend(ip_list)
        return result
    except FromatError,e:
        logging.error(str(e))
        return []


def formatIpRange(ipRange):
    format_pattern = '[\s;,]+'
    ipRange = re.sub(format_pattern, ',', ipRange)
    ipRange = ipRange.strip(',')
    return ipRange


def convt2cidr(ipstring):
    '''usage : convert to cidr range fromat.
       input : '1.0-255.*.*'
       output: ['1.0.0.0/8']
    '''
    try:
        ipaddress = IPAddress(ipstring)
        obj = ipaddress.contain
        small = obj[0][1].get_min(rtnum=True)
        big = obj[0][1].get_max(rtnum=True)
        rt_cidr = to_cidr(small, big)
        rt_str = []
        for x in rt_cidr:
            rt_str.append('%s/%d' % (long2ipv4(x[0]), x[1]))
        return rt_str
    except FromatError,e:
        logging.error(str(e))
        return []

def convtRange2cidr(start_str, end_str):
    '''usage : convert to cidr range fromat. 
       input : start_str '1.1.1.1' 
               end_str '1.1.1.2' 
       output: ['1.1.1.1/31']
    '''
    small = ip2long(start_str)
    big = ip2long(end_str)
    rt_cidr = to_cidr(small, big)
    rt_str = []
    for x in rt_cidr:
        rt_str.append('%s/%d' % (long2ipv4(x[0]), x[1]))
    return rt_str

def ipToSpan(ipRange):
    try:
        ipaddress = IPAddress(ipRange)
        rt_span = ipaddress.get_range()
        return rt_span[0]
    except FromatError,e:
        logging.error(str(e))
        return [-1, -1]

def ipFromSpan(span):
    if span  == [-1, -1]:
        return []
    small, big = span
    ip_small = long2ipv4(small)
    ip_big = long2ipv4(big)
    # if ip_small == ip_big:
    #     return ip_big
    return '%s-%s' % (ip_small, ip_big)


if __name__ == "__main__":
    #test = Single('192.168.1.1')
    #test_getDifferenceIRange()
    #print getIPList('1.0.1.255-255,1.0.1.250-255')
    #print Glob.validate('1.2.*.*')
    print getIPRangeBoundList('255.2.1.1')
    print getIPRangeBoundList('*.*.*.*', True)
    print getIPRangeBoundList('255.1.1.*,0.2.2.*')
    print convt2cidr('0.0-255.*.*')
    print ipv42long('255.255.255.255')