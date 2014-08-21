#!/usr/bin/env python
# --coding:Utf-8
import os
import sys
import time

import logging
import v4_utils

class IPBase(object) :
    def __init__(self , ipstring, start, end, count) :
        self.ipstring = ipstring
        self.start = start
        self.end = end
        self.count = count
        self.index = 0

    def validate(self) :
        pass
    
    def get_min(self) :
        pass
    
    def get_max(self) :
        pass
    
    def get_range(self, rtnum=False) :
        if rtnum:
            return [self.start, self.end]
        start_str = v4_utils.long2ip(self.start)
        end_str = v4_utils.long2ip(self.end)
        return [start_str, end_str]
    
    def get_next(self, n=1):
        if n is 1:
            if self.index < self.count:
                self.index += 1
            else:
                self.index = 0
                return None
        else:
            if n <= 0 or n > self.count:
                return None
            self.index = n
        rtnum = self.start + self.index - 1
        return v4_utils.long2ip(rtnum)
    
    def include(self , ip) :
        if isinstance(ip, str) :
            _ip = v4_utils.ip2long(ip)
        elif isinstance(ip , unicode) :
            _ip = v4_utils.ip2long(str(ip))
        else:
            _ip = ip
        if _ip >= self.start and _ip <= self.end:
            # print ip
            return True
        return False 

    def __sub__(self, obj):
        rt = v4_utils.get_difference([self.start, self.end], [obj.start, obj.end])
        return v4_utils.combine(rt)
