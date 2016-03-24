#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------
#  FileName    :	iptxt_create.py 
#  Author      :    wuqingfeng@
#  Date        :    2016-03-24
# -----------------------------------------------------

import json
import requests
import time

login_pw = {
    "username": "",
    "password": ""
}

page_num = 50

def get_access_token():
    headers = {'content-type': 'application/json'}
    url = "http://api.zoomeye.org/user/login"
    r = requests.post(url, data=json.dumps(login_pw), headers=headers)
    data_json = r.json()
    access_token = data_json.get("access_token")
    return access_token

def get_host_ips(access_token, start_num=23):
    headers = {'Authorization': 'JWT %s'%access_token}
    #url_str = 'http://api.zoomeye.org/host/search?query="port:6379"&page=%s'
    url = 'http://api.zoomeye.org/host/search'
    with open('ip.txt', 'w') as file:
        file.truncate()
    num = 0
    for i in range(start_num, page_num):
        num = i + 1
        params = {
                'query': 'port:6379',
                'page': num
            }
        print url, params
        #r = requests.get(url, headers=headers)
        try:
            r = requests.get(url, params=params, headers=headers)
            data_json = r.json()
            match_list = data_json.get('matches', [])
            with open('ip.txt', 'a') as file:
                #file.truncate()
                for match in match_list:
                    ip = match.get('ip')
                    file.write(ip+'\n')
        except Exception, e:
            print e
            print r.text.encode('utf-8')
            access_token = get_access_token()
            get_host_ips(access_token, num)
            break

        time.sleep(3)
        

if __name__=='__main__':
    access_token = get_access_token()
    get_host_ips(access_token)

