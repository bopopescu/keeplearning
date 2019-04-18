#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : redis_tools.py
# Author    : wuqingfeng@

import redis
# from settings import redis_url


def convert_kwargs(kwargs):
    new_kwargs = {}
    for k, v in kwargs.items():
        if isinstance(k, basestring):
            new_kwargs[k.lower()] = v
    return new_kwargs


class RedisClient(object):

    """
    Singleton pattern
    http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern
    """

    __instance = {}
    __rclis = {}

    def __new__(cls, **kwargs):
        kwargs = convert_kwargs(kwargs)
        if str(kwargs) not in cls.__instance:
            if 'url' in kwargs:
                pool = redis.ConnectionPool.from_url(**kwargs)
            else:
                pool = redis.ConnectionPool(**kwargs)
            cls.__rclis[str(kwargs)] = redis.StrictRedis(connection_pool=pool)
            cls.__instance[str(kwargs)] = super(RedisClient, cls).__new__(cls, **kwargs)
        return cls.__instance[str(kwargs)]

    def __init__(self, **kwargs):
        kwargs = convert_kwargs(kwargs)
        self.rcli = self.__rclis[str(kwargs)]

    @property
    def __dict__(self):
        try:
            return self.rcli.__dict__
        except RuntimeError:
            raise AttributeError('__dict__')

    def __dir__(self):
        try:
            return dir(self.rcli)
        except RuntimeError:
            return []

    def __getattr__(self, name):
        if name == '__members__':
            return dir(self.rcli)
        return getattr(self.rcli, name)


# rclient = RedisClient(url=redis_url)