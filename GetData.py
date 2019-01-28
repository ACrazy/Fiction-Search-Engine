# -*- coding: utf-8 -*-
import requests
import urllib.request
import re
import json

geader = '1'
# page = '1'
subject = {}

# url = 'https://www.readnovel.com/all?gender=' + geader + '&pageNum=' + page
URL = 'https://www.qidian.com/all?page=2'

def paPage(url, page):
    strJson = []
    res = urllib.request.urlopen(url)
    html = res.read().decode('utf-8')
    li = re.findall(r'<li>([\s\S]*?)</li>', html)#匹配
    for i in range(2,len(li)):
        img = re.findall(r'<img src="([\s\S]*?)"', li[i])
        title = re.findall(r'alt="([\s\S]*?)"', li[i])
        author = re.findall(r'<a class="default">([\s\S]*?)</a>', li[i])
        geners = re.findall(r'<span class="org">([\s\S]*?)</span>', li[i])
        state = re.findall(r'<span class="red">([\s\S]*?)</span>', li[i])
        count = re.findall(r'<span class="blue">([\s\S]*?)</span>', li[i])
        content = re.findall(r'<p class="intro">([\s\S]*?)</p>', li[i])
        subject = {'title': title, 'img': img, 'author': author, 'geners': geners, 'state': state, 'count': count, 'content': content}
        strJson.append(subject)

    fileUrl = 'file/' + page + '.txt'
    f = open(fileUrl,'w',encoding='utf-8')
    novelJson = {'subjects': strJson}
    # JsonStr = json.dumps(novelJson)
    f.write(str(novelJson))
    f.close()

def fuck(gg):
    for i in range(gg, 8759):
        try:
            page = str(i)
            url = 'https://www.readnovel.com/all?gender=' + geader + '&pageNum=' + page
            paPage(url, page)
            print(i)
        except:
            print('error:', i)
            fuck(i + 1)

fuck(1)


















