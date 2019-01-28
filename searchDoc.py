# -*- coding: utf-8 -*-
import invertedIndex as iv
import pymysql
import re
import math
import json

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='novels',charset='utf8')
cur = conn.cursor()

#搜索输入关键词后匹配到的文档索引，输入为列表
def searchIndex(input):
    searchList = []
    docList = []
    segList = iv.tokenizer(input)
    outputWord = segList[0].split('/')
    print(outputWord)

    for word in outputWord:
        try:
            sql = "select wordIndex from inverted WHERE word = " + '\'' + word + '\''
            cur.execute(sql)
            searchList.append(str(cur.fetchall()[0]).replace(',)', '').replace('\'', '').replace('(', ''))
        except:
            searchList.append('')
            continue
    # for r in cur:
    #     print("row_number:" , (cur.rownumber) )
    #     print("id:"+str(r[0])+"name:"+str(r[1])+"wordIndex:"+str(r[2]))
    return outputWord,searchList

def tf_idf(docNum, docMartix, idf, segDoc):
    tfidf = []
    for i in range(1, len(docNum)):
        tfidfmatix = []
        tfidfmatix.append(docNum[i])
        for j in range(len(segDoc)):
            point = True
            for matix in docMartix:
                if matix[3] == segDoc[j] and matix[0] == docNum[i]:
                    point = False
                    tf = matix[1]
                    TFIDF = float(tf) * idf[j]
                    tfidfmatix.append(TFIDF)
                    break
            if point:
                tfidfmatix.append(0)
        tfidf.append(tfidfmatix)
    return tfidf

def IDF(docNum, indexList):
    Idf = []
    for index in indexList:
        if index != '':
            temp = index.split('&')
            idf = math.log(int(docNum)/len(temp))
        else:
            idf = 1
        Idf.append(idf)
    return Idf

def docMatrix(input):
    num = ['yzs']
    idf = []

    outputWord,docList = searchIndex(input)
    docNum_TF_Pos = []
    for i in range(len(docList)):
        if docList[i] != '':
            docNum = re.findall(r'<([\s\S]*?);', docList[i])
            tf = re.findall(r';([\s\S]*?);', docList[i])
            position = re.findall(r'\[([\s\S]*?)\]', docList[i])
            idf.append(len(docNum))
            for j in range(len(docNum)):
                doc = []
                doc.append(docNum[j])
                doc.append(tf[j])
                doc.append(position[j])
                doc.append(outputWord[i])
                docNum_TF_Pos.append(doc)
        else:
            idf.append(0)
    for temp in docNum_TF_Pos:
        point = True
        for top in num:
            if top == temp[0]:
                point = False
                break
        if point:
            num.append(temp[0])
    return docNum_TF_Pos,num,docList,outputWord  #['11', '2', '17,18', '世界'],['yzs', '1', '3', '5', '8', '11', '4', '10']

def input_tf_idf(outputWord, IDF):
    tfidf = []
    for i in range(len(outputWord)):
        TF = 0
        for temp in outputWord:
            if outputWord[i] == temp:
                TF += 1
        # print(TF)
        TFIDF = TF * IDF[i]
        tfidf.append(TFIDF)
    return tfidf

def cos(inputMatix, docMatix):
    docCosine = []
    for matix in docMatix:
        coo = []
        coo.append(matix[0])
        top = 0.0
        inputDown = 0.0
        matixDown = 0.0

        for i in range(len(inputMatix)):
            top += inputMatix[0] * matix[i+1]
            inputDown += inputMatix[i] * inputMatix[i]
            matixDown += matix[i+1] * matix[i+1]

        cosine = top/(math.sqrt(inputDown)*math.sqrt(matixDown))
        coo.append(cosine)
        docCosine.append(coo)

    return docCosine

def weight(outputword, docCosine, input):
    print('now weighting...')
    weight = 0.0
    docwei = []

    for i in range(len(docCosine)):
        docCos = []
        sql = "select title, author, geners, state, counts, content, img from novels WHERE Id = " + docCosine[i][0]
        cur.execute(sql)
        abc = cur.fetchone()
        # print(abc[0],abc[1])
        weight = docCosine[i][1]
        for word in outputword:
            if abc[0] == input[0]:
                weight += 10.0
            if abc[0].startswith(input[0]):
                weight += 5.0
            if abc[1] == input[0]:
                weight += 10.0
            if abc[1].startswith(input[0]):
                weight += 5.0
            if word in abc[0]:
                weight += 1.0
            if word in abc[1]:
                weight += 0.5
        docCos.append(weight)
        docCos.append(abc[0])
        docCos.append(abc[1])
        docCos.append(abc[2])
        docCos.append(abc[3])
        docCos.append(abc[4])
        docCos.append(abc[5])
        docCos.append(abc[6])
        docwei.append(docCos)
        # print(docCosine)
    return docwei

def search(input):
    result = []

    docTomartix, docNum, docIndex, outputWord = docMatrix(input)
    idf = IDF(len(docNum), docIndex)
    docTFIDF = tf_idf(docNum, docTomartix, idf, outputWord)
    inputTFIDF = input_tf_idf(outputWord, idf)

    docCosine = cos(inputTFIDF, docTFIDF)
    docName = weight(outputWord, docCosine, input)
    docWeight = sorted(docName, key=lambda x:x[0], reverse=True)

    try:
        for i in range(10):
            result.append(docWeight[i])
            print(docWeight[i])
    except:
        for doc in docWeight:
            result.append(docWeight[i])
            print(doc)
    # print(len(docWeight))


    return result



# x = input('please input：')
# input1 = []
# input1.append(x)
# docWeight = search(input1)
# try:
#     for i in range(10):
#         print(docWeight[i])
# except:
#     for doc in docWeight:
#         print(doc)
# input = ["斗罗大陆"]
# docWeight = search(input)
# try:
#     for i in range(10):
#         print(docWeight[i])
# except:
#     for doc in docWeight:
#         print(doc)
# print(docTFIDF)
# print(inputTFIDF)
# print(docTomartix)
# print(docNum)
# print(docIndex)
# print(idf)






