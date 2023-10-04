
# 同一个pattern去重了，但是不同pattern随机生成的ip地址也可能重合，因此需要再去一次重！！！

source = 'output.txt'
target = 'output_unique.txt'
fi = open(source, 'r') # 打开需要处理的test.txt。
line = fi.read()
fi.close()

line_list = line.split('\n')
line_list_set = list(set(line_list))

wr = open(target,'w')
for s in line_list_set:
    wr.write(s+'\n')
    
wr.close()

print(len(line))
print(len(line_list))
print(len(line_list_set))
