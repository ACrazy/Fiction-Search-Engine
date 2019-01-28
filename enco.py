# -*- coding: utf-8 -*-
import json
import re
import xlrd
import xlwt
from xlutils.copy import copy
import os

new_excel = xlrd.open_workbook('12.xlsx')
new_excel_copy = copy(new_excel)
# 获得sheet的对象
new_sheet = new_excel.sheet_by_name('Sheet1')
new_excel_copysheet = new_excel_copy.get_sheet(0)

number = 1
array = []

def saveFile(url, number):
    # page = 2586
    # url = 'file3/' + str(page) + '.txt'
    f = open(url, 'r', encoding='utf-8')
    data = f.read()
    data = re.sub('\'','\"',data)

    strJson = eval(data)
    # strJson = data['subjects'][1]['title'][0]
    for i in range(0, len(strJson['subjects'])):
        new_excel_copysheet.write(number + i, 0, strJson['subjects'][i]['title'][0].strip().replace('\r\n', '').replace('\n', ''))
        new_excel_copysheet.write(number + i, 1, strJson['subjects'][i]['author'][0].strip().replace('\r\n', '').replace('\n', ''))
        new_excel_copysheet.write(number + i, 2, strJson['subjects'][i]['geners'][0].strip().replace('\r\n', '').replace('\n', ''))
        new_excel_copysheet.write(number + i, 3, strJson['subjects'][i]['state'][0].strip().replace('\r\n', '').replace('\n', ''))
        new_excel_copysheet.write(number + i, 4, strJson['subjects'][i]['count'][0].strip().replace('\r\n', '').replace('\n', ''))
        new_excel_copysheet.write(number + i, 5, strJson['subjects'][i]['content'][0].strip().replace('\r\n', '').replace('\n', '').replace(' ', ''))
        new_excel_copysheet.write(number + i, 6, strJson['subjects'][i]['img'][0].strip().replace('\r\n', '').replace('\n', ''))
    f.close()
    # print(len(strJson['subjects']))
    print('yeah')
    return len(strJson['subjects'])

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root) #当前目录路径
        # print(dirs) #当前路径下所有子目录
        return files #当前路径下所有非目录子文件


# for i in range(8000, 14770):
#     count = saveFile(i, number)
#     if count == 0:
#         array.append(i)
#         # print(i)
#     else:
#         number += count
for name in file_name('file4'):
    url = 'file4/' + name
    count = saveFile(url, number)
    if count == 0:
        array.append(name)
        # print(i)
    else:
        number += count
# print(saveFile(30, number))
# print(file_name('file3'))





print(array)
new_excel_copy.save('test7.xls')
print("finish")