

from OutlierDetection import OutlierDetect
from SpacePartition import *
from OutlierDetection import *
from SpacePartition import show_regions
from germinate_data import random_gernerate
from convert import convert
import time
from ActiveScan import scan_addr
import random
import sys

def num_sort(C):
    m = [] 
    n = []
    temp = []
    for x in C:
        m.append(len(x))
        n.append(len(x))
    m.sort(reverse=False)
    index = 0
    for i in m:
        temp.append(C[n.index(i)])
        n[n.index(i)] = []
    
    return temp

def Start(input,output):
    
    a = output+'/data.txt'
    os.makedirs(os.path.dirname(a),exist_ok=True)
    convert(input,output)
    data = np.load(output+"/data.npy")

    modules = []
    samples = []
    results = DHC(data)
    
    count = 1
    patterns_count = 0
    
    for r in results:
        c, m,s = OutlierDetect(r)
        if c !=0:
            count+=1
        patterns_count += c
        modules+=m
        samples+=s
    

    # print(patterns_count)
    f1 = open(output+'/ordinary_patterns.txt', "w")    
    # f1.write("real pattern_count: "+str(patterns_count)+'\n')
    f1.write(str(modules))
    f1.close()

    f2 = open(output+'/ordinary_samples.txt',"w")
    # sys.stdout = f2
    # print(len(samples))
    f2.write(str(samples))
    f2.close()


def generate_test(input,sub_output,budget,output):
    
    a = output+'/data.txt'
    os.makedirs(os.path.dirname(a),exist_ok=True)

    filename = sub_output+'/generate_samples.txt'
    os.makedirs(os.path.dirname(filename),exist_ok=True)
    f = open(filename,"w")
    
    test_data=set()
    modules = eval(open(output+'/ordinary_patterns.txt','r').read())
    samples = eval(open(output+'/ordinary_samples.txt','r').read())

    origin_budget = budget
    # budget = int(budget*1.1)
    
    single_pattern_budget = (int(budget/len(modules))+1)
    print('开始生成样本')
    test_data_origin = random_gernerate(modules,samples,budget)
    print("生成的样本数：",len(test_data_origin))
    # f2 = open(output+'/ordinary_samples.txt',"w")
    # f2.write(test_data_origin)
    # f2.close()
    # for i in test_data_origin:
    #     print(len(i))

    test_data_more = []
    for t in test_data_origin:
        if(len(t)<=single_pattern_budget):
            test_data = test_data|set(t)
        else :
            test_data_more.append(t)
    
    if len(test_data) > budget:
        test_data = random.sample(test_data,budget)
    else:
        x = len(test_data_more)
        # for i in test_data_more:
        #     print(len(i))
        test_data_more = num_sort(test_data_more)
        
        for t in range(len(test_data_more)):
            
            if x == 1:
                rest = int ((budget - len(test_data))/x)
            else :
                rest = int ((budget - len(test_data))/x)+1
            if rest <= 0 :break
            if(rest>=len(test_data_more[t])):
                test_data |= set(test_data_more[t])
                x = x-1
            else :
                test_data |= set(random.sample(test_data_more[t],rest))
                x = x-1

    # file_test = sub_output+'/file_test.txt'
    # # test_data = eval(open(file_test,'r').read())
    # os.makedirs(os.path.dirname(file_test),exist_ok=True)
    # ff = open(file_test,"w")
    # ff.write(str(test_data))
    # ff.close()


    # 去别名
    # print("去别名前的长度：",len(test_data))
    # test_data = alias_fun(test_data,sub_output)
    
    print("长度：",len(test_data))
    if len(test_data) > origin_budget:
        test_data = random.sample(test_data,origin_budget)
    print("最终的长度：",len(test_data))

    for d in test_data:
        f.write(d+"\n")
    # f.write(str(len(test_data)))
    f.close()
    
    if len(test_data)<1:
        return (0,0,0)
    else :
        print(input+" 生成了target num : "+str(len(test_data)))
    
    
    # do something for the seed region list,  i.e., patterns
    # Note the Outliers can be used for the next iter input
