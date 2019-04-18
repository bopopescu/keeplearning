#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : main.py
# Author    : wuqingfeng@


from example import person_pb2

if __name__ == '__main__':
    pers = person_pb2.all_person()
    p1 = pers.Per.add()
    p1.id = 1
    p1.name = 'lihai'
    p2 = pers.Per.add()
    p2.id = 2
    p2.name = 'niubi'
    print "pers: ", pers
    data = pers.SerializeToString()
    # print 'data: ', data
    target = person_pb2.all_person()
    target.ParseFromString(data)
    print target, target.Per[1].name
