### 1

使用get_dataset.py来选择一部分总数据集作为测试数据集

### 2

从测试数据集中挖掘模式

```Shell
python patternMining.py --read ./part_dataset.txt --budgets 10000 --write ./1 --limit 4
```

### 3

使用trans.py将得到的pattern转为一系列ipv6地址

### 4

运行zmap进行地址扫描

出现地址识别错误可能需要使用dos2unix将target文件转为unix格式。