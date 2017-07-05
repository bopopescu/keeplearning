#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : ciacrawler.py
# Author    : wuqingfeng@

import requests
import re
import time
import datetime
from bs4 import BeautifulSoup
from esclient import esclient

url_prefix = "http://10.5.0.190:8080/year0/vault7/cms/"
cat = "index.html"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
# urls = []

if __name__ == "__main__":
    url_index = url_prefix + cat
    html = requests.get(url_index, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    tag_list = soup.select("div#uniquer > ul > h3")
    table_list = soup.select("div#uniquer > ul > table")
    # print table_list[0].select("td > a")
    for i in range(len(tag_list)):
    # for i in [0]:
        tag_name = tag_list[i].text
        print tag_name
        page_list = table_list[i].select("div[style] > a")
        # page_list = page_list[:1]
        # print page_list
        count = 0
        for page in page_list:
            count = count + 1 
            print "start to crawl the page %s" % count
            page_path = page['href']
            # page_title = page.text
            page_url = url_prefix + page_path
            print page_url
            page_html = requests.get(page_url, headers=headers).text
            page_soup = BeautifulSoup(page_html, 'html.parser')
            try:
                page_title = ' '.join(list(page_soup.select("div#uniquer > h2")[0].stripped_strings))
            except:
                page_title = page.text
            content_list = page_soup.select("div#uniquer")
            string_list = []
            for content in content_list:
                content_gen = content.stripped_strings
                string_list.extend(list(content_gen))
            string_content = ' '.join(string_list)
            es_json = {
                "tag": tag_name,
                "page_url": page_url,
                "page_title": page_title,
                "content": string_content
            }
            esclient.index(index='cia-index', doc_type='ciareport', op_type='index', timestamp=datetime.datetime.now(), body=es_json)
            time.sleep(0.5)

