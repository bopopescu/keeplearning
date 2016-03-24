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

page_num = 100

def get_access_token():
    headers = {'content-type': 'application/json'}
    url = "http://api.zoomeye.org/user/login"
    r = requests.post(url, data=json.dumps(login_pw), headers=headers)
    data_json = r.json()
    access_token = data_json.get("access_token")
    return access_token

def get_host_ips(access_token):
    headers = {'Authorization': 'JWT %s'%access_token}
    url_str = 'http://api.zoomeye.org/host/search?query="port:6379"&page=%s'
    with open('ip.txt', 'w') as file:
        file.truncate()
    for i in range(page_num):
        num = i + 1
        url = url_str % num
        print url
        r = requests.get(url, headers=headers)
        try:
            data_json = r.json()
            match_list = data_json.get('matches', [])
            with open('ip.txt', 'a') as file:
                #file.truncate()
                for match in match_list:
                    ip = match.get('ip')
                    file.write(ip+'\n')
        except Exception, e:
            print e
            print r.text
        
        time.sleep(10)

if __name__=='__main__':
    access_token = get_access_token()
    get_host_ips(access_token)

