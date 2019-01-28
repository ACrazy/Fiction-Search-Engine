# -*- coding: utf-8 -*-
import pymysql
import xlrd
import invertedIndex as iv

docUrl = 'doc/no.xlsx'
url = 'doc/fuckme.txt'

#get all doc
docList = []
position = []
wordT = []
print('now get all doc...')

#connnect db
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='novels',charset='utf8')
cur = conn.cursor()

position,wordT = iv.readAlldocindex(url)

# f = open('save/index.txt', 'r', encoding='utf-8')
# file = f.read()
# docList = file.split('\n')
# for i in docList:
#     if i != '':
#         temp = i.replace(',<', '!<').split('!')
#         wordT.append(temp[0])
#         position.append(temp[1])

for i in range(0, len(position)):
    sql = ""
    print('insert word', wordT[i])
    sql += '\'' + wordT[i] + '\'' + ', ' + '\'' + position[i] + '\''
    sql = "insert into invertedindex(word,wordindex) values(" + sql + ")"
    cur.execute(sql)
    conn.commit()

# sql = "truncate table invertedindex"
# cur.execute(sql)
# conn.commit()
cur.close()
conn.close()












