# -*- coding:utf-8 -*-
#在txt文件中随机抽取行
import random
from random import randint
 
oldf = open('output.txt', 'r',encoding='utf-8')    #要被抽取的文件dataset.txt，共5000行
newf = open('output_100w.txt', 'w',encoding='utf-8')   #抽取的2000行写入randomtext.txt
n = 0
resultList = random.sample(range(0, 11672834), 1100000)  # sample(x,y)函数的作用是从序列x中，随机选择y个不重复的元素
 
lines = oldf.readlines()
for i in resultList:
    newf.write(lines[i])
oldf.close()
newf.close()
