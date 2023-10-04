from tqdm import tqdm

with tqdm(total=1000) as pbar:
    for i in range(10):
        pbar.update(1)


# 读入一个txt to pāndas
# import pandas as pd

f =  open('Baseline/AddrMiner/result_dateset1/budget_no100/result-N.txt', 'r').readlines()
a = len(f)
f =  open('Baseline/AddrMiner/result_dateset1/budget_no100/target-N.txt', 'r').readlines()
b = len(f)
print(a, b)
print(a/b)
# data = [i.split(',')[1] for i in f]
# print(data[0])

