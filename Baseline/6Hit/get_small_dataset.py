import random
f = open('Baseline/Database/dataset1.txt','r').readlines()
data = [i.strip() for i in f]
num = 5000
data_select = random.sample(data,num)
with open('Baseline/Database/dataset1_{}.txt'.format(num),'w') as f:
   f.write('\n'.join(data_select))
