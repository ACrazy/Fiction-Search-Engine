import math
import numpy

def txtToList(FileUrl):
    list = []
    file = open(FileUrl, 'r')
    for line in file.readlines():
        list.append(line.strip())
    return list

def sum(file, temp):
    search_TF = 0
    engine_TF = 0
    index_TF = 0

    for word in file:
        if temp[0] == word:
            search_TF += 1
        if temp[1] == word:
            engine_TF += 1
        if temp[2] == word:
            index_TF += 1
    doc = [search_TF, engine_TF, index_TF]
    return doc

def TF(file, temp):
    doc = sum(file, temp)
    docTF = []

    for tf in doc:
        if tf > 0:
            tf = 1 + math.log(tf)
        else:
            tf = 0
        docTF.append(tf)
    return docTF

def IDF(file1, file2, file3):
    search_IDF = 0
    engine_IDF = 0
    index_IDF = 0

    for i in range(3):
        if i == 0:
            if file1[i] != 0:
                search_IDF += 1
            if file2[i] != 0:
                search_IDF += 1
            if file3[i] != 0:
                search_IDF += 1
        if i == 1:
            if file1[i] != 0:
                engine_IDF += 1
            if file2[i] != 0:
                engine_IDF += 1
            if file3[i] != 0:
                engine_IDF += 1
        if i == 2:
            if file1[i] != 0:
                index_IDF += 1
            if file2[i] != 0:
                index_IDF += 1
            if file3[i] != 0:
                index_IDF += 1
    search_IDF = math.log(3/search_IDF)
    engine_IDF = math.log(3/engine_IDF)
    index_IDF = math.log(3/index_IDF)
    return [search_IDF, engine_IDF, index_IDF]

def cos(x, y):
    top = x[0]*y[0] + x[1]*y[1] + x[2]*y[2]
    down = math.sqrt(pow(x[0],2) + pow(x[1],2) + pow(x[2],2)) * math.sqrt(pow(y[0],2) + pow(y[1],2) + pow(y[2],2))
    return top/down

file_1 = txtToList('file1.txt')
file_2 = txtToList('file2.txt')
file_3 = txtToList('file3.txt')

query = ['search', 'engine', 'index']

docTF_1 = TF(file_1, query)
docTF_2 = TF(file_2, query)
docTF_3 = TF(file_3, query)

fileSum_1 = sum(file_1, query)
fileSum_2 = sum(file_2, query)
fileSum_3 = sum(file_3, query)

fileIDF = IDF(fileSum_1, fileSum_2, fileSum_3)

docVector_1 = [docTF_1[0]*fileIDF[0], docTF_1[1]*fileIDF[1], docTF_1[2]*fileIDF[2]]
docVector_2 = [docTF_2[0]*fileIDF[0], docTF_2[1]*fileIDF[1], docTF_2[2]*fileIDF[2]]
docVector_3 = [docTF_3[0]*fileIDF[0], docTF_3[1]*fileIDF[1], docTF_3[2]*fileIDF[2]]

queryVector = [1.0*fileIDF[0], 1.0*fileIDF[1], 1.0*fileIDF[2]]

print("query与文档一的余弦相似度：", cos(queryVector, docVector_1))
print("query与文档二的余弦相似度：", cos(queryVector, docVector_2))
print("query与文档三的余弦相似度：", cos(queryVector, docVector_3))
#print(queryVector)