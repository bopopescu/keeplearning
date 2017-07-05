#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : taomm_spider.py
# Author    : wuqingfeng@

import urllib
import urllib2
import re
import time

class Tool(object):
    #去除img标签,1-7位空格,&nbsp;
    removeImg = re.compile('<img.*?>| {1,7}|&nbsp;')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    #将多行空行删除
    removeNoneLine = re.compile('\n+')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = re.sub(self.removeNoneLine,"\n",x)
        #strip()将前后多余内容删除
        return x.strip()

class Spider(object):

    def __init__(self):
        self.siteURL = 'https://mm.taobao.com/json/request_top_list.htm'
        self.tool = Tool()
        self.number = 0

    @staticmethod
    def saveImg(imageURL, fileName):
        image = urllib2.urlopen(imageURL)
        data = image.read()
        with open(fileName, 'wb') as f:
            f.write(data) 

    @staticmethod
    def saveBrief(content, name):
        fileName = name + "/" + name + ".txt"
        with open(fileName, 'w+') as f:
            f.write(content.encode('utf-8'))

    @staticmethod
    def mkdir(path):
        path = path.strip()
        isexists = os.path.exists(path)
        if not isexists:
            os.makedirs(path)
            return True
        else:
            return False

    def getContents(self, pageIndex):

        def getPage(pageIndex):
            url = self.siteURL + "?page=" + str(pageIndex)
            print url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('gbk')

        page = getPage(pageIndex)
        match_str = r'<div class="list-item".*?pic-word.*?<a href="//(.*?)".*?<img src="//(.*?)".*?<a class="lady-name" href="//(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>'
        pattern = re.compile(match_str, re.S)
        items = re.findall(pattern, page)
        # print items
        return items

    def getDetailPage(self, infoURL):
        infoURL = "http://" + infoURL
        print infoURL
        response = urllib2.urlopen(infoURL)
        return response.read().decode('gbk')

    def getBrief(self, page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern, page)
        return self.tool.replace(result.group(1))

    def getAllImg(self, page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        content = re.search(pattern,page)
        patternImg = re.compile('<img.*?src="(.*?)"',re.S)
        images = re.findall(patternImg,content.group(1))
        return images

    @staticmethod
    def saveImgs(images, name):
        number = 1
        print u"find the %s have %s pictures" % (name, len(images))
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            Spider.saveImg(imageURL, fileName)
            number += 1

    @staticmethod
    def saveIcon(iconURL, name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        saveImg(iconURL, fileName)

    def savePageInfo(self, pageIndex):
        contents = self.getContents(pageIndex)
        for item in contents:
            #item[0]个人详情URL,item[1]头像URL,item[2]信息URL, item[3]名字, item[4]年龄,item[5]居住地
            self.number += 1
            info = u"No.%s 名字: %s, 年龄: %s, 所在地: %s, icon: %s, 详细信息: %s, 图片URL: %s \r\n" %(self.number, item[3], item[4], item[5], item[1], item[2], item[0])
            print info
            with open("info.txt", "a+") as f:
                f.write(info.encode('utf-8'))
            # detailURL = item[0]
            # try:
            #     detailPage = self.getDetailPage(detailURL)
            #     # print detailPage
            #     brief = self.getBrief(detailPage)
            #     images = self.getAllImg(detailPage)
            #     Spider.mkdir(item[3])
            #     Spider.saveBrief(brief,item[3])
            #     Spider.saveIcon(item[1],item[3])
            #     Spider.saveImgs(images,item[3])
            # except Exception, e:
            #     print e
            #     print detailPage
            # time.sleep(0.5)

    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            self.savePageInfo(i)

if __name__ == '__main__':
    spider = Spider()
    # spider.getContents(1)
    spider.savePagesInfo(1, 100000)