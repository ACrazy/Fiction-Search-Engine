# 本项目Python3.5
- cmd运行python flaskTest.py启动项目

**目录：**
- GetData.py 数据爬取
- invertedIndex.py 数据预处理
- pyDB.py 连接数据库，并且存储各个小说条目的索引
- searchDoc.py 通过tfidf、关键词权重、文本余弦相似度计算搜索query和数据库数据进行匹配
