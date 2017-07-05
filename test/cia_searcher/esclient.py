#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : esclient.py
# Author    : wuqingfeng@

from elasticsearch import Elasticsearch

__all__ = ['ESClient']

class ESClient(Elasticsearch):
    """
    Singleton pattern
    http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern
    """

    __instance = {}

    def __init__(self, **kwargs):
        if str(kwargs) not in self.__instance:
           self.__instance[str(kwargs)] = super(ESClient, self).__init__(**kwargs)
        return self.__instance[str(kwargs)]

esconfig = {
    "hosts": [{'host': '10.5.0.85', 'port': 9200}],
    "timeout": 300,
    "maxsize": 25
}

esclient = ESClient(**esconfig)

if __name__ == '__main__':
    esclient.indices.create(index='cia-index', ignore=400)