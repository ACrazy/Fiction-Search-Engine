# -*- coding: utf-8 -*-
import xlrd
import jieba
import json


# docUrl = 'doc/novelstest.xlsx'
# saveUrl = 'doc/fuck.txt'
# url = 'doc/fuck.txt'

#获取所有文档
def getDoc(url):
    docList = []
    print('now get all doc...')
    new_excel = xlrd.open_workbook(url)
    # 获得sheet的对象
    new_sheet = new_excel.sheet_by_name('Sheet1')
    for i in range(1, new_sheet.nrows):
        temp = ""
        for j in range(6):
            temp += new_sheet.cell_value(i, j)
        docList.append(temp)
    print('get doc done!')
    return docList

# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

#分词、去停
def tokenizer(docList):
    stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径
    docKeywords = []
    num = 1
    print('now tokenizer doc...')

    for doc in docList:
        num += 1
        print('tokenizerdoc', num)
        seg_list = jieba.cut(doc, cut_all=False)
        outstr = ''
        for word in seg_list:
            if word not in stopwords:
                if word != '\t' and word != '\r\n' and word != '\n' and word != '　' and word != '\r':
                    outstr += word
                    outstr += "/"
        docKeywords.append(outstr[:-1])
    print('Done!')
    return docKeywords

#统计词频
def TF(doc):
    array = '{'
    for word in doc:
        count = 0
        wordList = []
        countlist = []
        if word not in wordList:
            for temp in doc:
                if word == temp:
                    count += 1
            wordList.append(word)
            countlist.append(count)
            if word != '':
                array += '\'' + word  + '\''+ ': ' + str(count) + ', '
    array = array[:-2]
    array += '}'
    dict = eval(array)
    return dict

def invertedIndex(docList):
    index = []
    print("now invertedIndex...")

    for doc in range(len(docList)):
        print('doc', doc)
        docIndex = []
        temp = []
        position = []
        # outPosition = []
        keywords = docList[doc].split('/')
        docTF = TF(keywords)
        dict = docTF.keys()
        dictStr = '{'
        for i in range(len(keywords)):
            position.append(i+1)
            temp.append(keywords[i])
        for word in dict:
            outPosition = []
            for j in range(len(temp)):
                if word == temp[j]:
                    outPosition.append(position[j])
            dictStr += '\'' + word + '\''+ ': ' + '\'' + '<' + str(doc + 1) + ';' + str(docTF[word]) +  ';' + str(outPosition) + '>' + '\'' + ', '
            # docIndex.append(dictStr)
        dictStr = dictStr[:-2]
        dictStr += '}'
        index.append(dictStr)
    return index

def readAlldocindex(url):
    wordDict = []
    wordT = ['_yzs']
    position = ['_yzs']

    f = open(url, 'r', encoding='utf-8')
    file = f.read()
    file = file.replace('\n', '').replace('{', '').replace('}', ', ')
    wordIndex = file.split('\', ')
    for word in wordIndex:
        pont = True
        print(word)
        word = word.replace('\'', '').replace(' ','')
        wordTemp = word.split(':')
        for i in range(len(wordT)):
            if wordTemp[0] == wordT[i]:
                pont = False
                # for index in wordIndex:
                #     index = index.replace('\'', '').replace(' ','')
                #     indexTemp = index.split(':')
                #     if wordTemp[0] == indexTemp[0] and len(wordTemp) == 2 and len(indexTemp) == 2:
                #         strr += indexTemp[1] + '&'
                # print('check', wordTemp[0] + ':' + strr[:-1])
                # wordDict.append(wordTemp[0] + ':' + strr[:-1])
                if len(wordTemp) == 2:
                    position[i] = position[i] + '&' + wordTemp[1]
                break
        if pont:
            if len(wordTemp) == 2:
                position.append(wordTemp[1])
                wordT.append(wordTemp[0])

    f = open('save/index1.txt', 'w', encoding='utf-8')
    for i in range(1, len(wordT)):
        f.write(wordT[i] + ',' + position[i] + '\n')
    f.close()
    print('save done!')
    return position,wordT

# position,wordT = readAlldocindex(url)
# print(wordT[8])
# print(position[8])

# list = tokenizer(getDoc(docUrl))
# ll = invertedIndex(list)
# strr = '绝世/药皇/永远/天涯/玄幻/连载中/545.22/万/特种兵/王杨风/转世/重生/废物/身上/受尽/嘲讽/不鸣则已/一鸣/惊人/不飞/一飞/冲天/武魂/觉醒/便是/强者/路/绝世/炼药/天赋/强者/尊/武魂/世界/中/强势/崛起/成就/一代/魂帝/绝世/药皇/'
# tt = strr.split('/')
# print(TF(tt))
# f = open(saveUrl, 'w', encoding='utf-8')
# for doc in ll:
#     f.write(doc + '\n')
# print('finish')





















