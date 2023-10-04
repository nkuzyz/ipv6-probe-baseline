
from SpacePartition import *
from PatternMining import *
from germinate_data import random_gernerate
import sys
import os,random
from convert import convert
from ActiveScan import scan_addr
 
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


def first_work():

    para = "entire"

    
    data = np.load("database/scan_output_responsive_"+para+".npy")
    filename ="output/result_"+para+"/"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # print("data length: "+str(len(data)))
    patterns = []
    outliers = []
    results = DHC(data)
    # print("spacepartition first: "+str(len(results)))
    for r in results:
        p, o = OutlierDetect(r)
        patterns += p
        outliers += o

    # 孤立出去的点再喂进去分类
    # 3. 6Graph exploits the graph-theoretic algorithm to mine the address patterns from the seed regions
    # while the misclassified seeds (outliers) in the seed regions will be removed. 
    # Meanwhile, some outliers will be attached to their zero-distance address patterns, i.e., seed rejoin-ing, 
    # while others will be used as the new seed sets for the next round.
    
    # your can seed the number of iter, usually < 5
    for _ in range(3):
        results = DHC(np.vstack(outliers))
        outliers = []
        for r in results:
            p, o = OutlierDetect(r)
            patterns += p
            outliers += o

    # display or directly use for yourself
    modules =[]
    samples =[]
    for index, p in zip(list(range(len(patterns))), patterns):
        Tarrs = p.T

        address_space = []

        for i in range(32):
            splits = np.bincount(Tarrs[i], minlength=16)
            if len(splits[splits > 0]) == 1:
                address_space.append(format(
                    np.argwhere(splits > 0)[0][0], "x"))
            else:
                address_space.append("*")
        # print("No.", index, "address pattern")
        # print("".join(address_space))
        modules.append("".join(address_space))
        # print("-"*32)
        samples=[]
        for iparr in p:
            # print("".join([format(x, "x") for x in iparr]))
            samples.append("".join([format(x, "x") for x in iparr]))
        samples.append(samples)
        # print()


    print("正式的找模式  算法完成，接下来打印数据然后生成数据的步骤开始了！！！！！！！")
    f1 = open(filename+'ordinary_patterns.txt', "w")    
    sys.stdout = f1
    for m in modules:
        print(m)
    print(len(modules))


    f2 = open(filename+'ordinary_samples.txt',"w")
    sys.stdout = f2
    f1.close()
    for s in samples:
        print(s)
    print(len(samples))
 
    # sys.stdout = open(filename+'generate_samples.txt',"w")
    # f2.close()


    # test_data = []
    # test_data = random_gernerate(modules,samples)
    # for d in test_data:
    #     print(d)
    # print(len(test_data))

        # show_regions(p)
    # print(len(modules))
    # print(len(samples))
    # print(len(test_data))



def Start(input,output):
    
    a = output+'/data.txt'
    os.makedirs(os.path.dirname(a),exist_ok=True)
    convert(input,output)
    data = np.load(output+"/data.npy")

    patterns = []
    outliers = []
    results = DHC(data)
    # print("spacepartition first: "+str(len(results)))
    for r in results:
        p, o = OutlierDetect(r)
        patterns += p
        outliers += o
    # your can seed the number of iter, usually < 5
    # print(outliers)
    for _ in range(3):
        if len(outliers) > 0:
            results = DHC(np.vstack(outliers))
            outliers = []
            for r in results:
                p, o = OutlierDetect(r)
                patterns += p
                outliers += o

    # display or directly use for yourself
    modules =[]
    samples =[]
    for index, p in zip(list(range(len(patterns))), patterns):
        Tarrs = p.T

        address_space = []

        for i in range(32):
            splits = np.bincount(Tarrs[i], minlength=16)
            if len(splits[splits > 0]) == 1:
                address_space.append(format(
                    np.argwhere(splits > 0)[0][0], "x"))
            else:
                address_space.append("*")
        # print("No.", index, "address pattern")
        # print("".join(address_space))
        modules.append("".join(address_space))
        # print("-"*32)
        temp_samples=[]
        for iparr in p:
            # print("".join([format(x, "x") for x in iparr]))
            temp_samples.append("".join([format(x, "x") for x in iparr]))
        samples.append(temp_samples)
        # print()

    

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
    
    return 1

def generate_test(input,sub_output,budget,output):
    filename = sub_output+'/generate_samples.txt'
    os.makedirs(os.path.dirname(filename),exist_ok=True)
    f = open(filename,"w")
    
    test_data=set()
    modules = eval(open(output+'/ordinary_patterns.txt','r').read())
    samples = eval(open(output+'/ordinary_samples.txt','r').read())
    print(str(len(modules))+'zyz')

    origin_budget = budget
    # budget = int(budget*1.1)
    single_pattern_budget = (int(budget/len(modules))+1)
    # test_data = random_gernerate(modules,samples,single_pattern_budget)
    # if len(test_data) > budget:
    #     test_data = random.sample(test_data,budget)
    print('开始生成样本')
    print(str(budget))
    test_data_origin = random_gernerate(modules,samples,budget)
    print("生成的样本数：",str(len(test_data_origin)))
    test_data_more = []
    for t in test_data_origin:
        if(len(t)<single_pattern_budget):
            test_data = test_data|set(t)
        else :
            test_data_more.append(t)
    
    if(len(test_data)>=budget):
        test_data = random.sample(test_data,budget)

    else:
        x = len(test_data_more)

        test_data_more = num_sort(test_data_more)
        
        for t in range(len(test_data_more)):
            
            if x == 1:
                rest = int ((budget - len(test_data))/x)
            else :
                rest = int ((budget - len(test_data))/x)+1
            if rest <= 0 :break
            if(rest >= len(test_data_more[t])):
                test_data |= set(test_data_more[t])
                x = x-1
            else:
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
    if(len(test_data)>origin_budget):
        test_data = random.sample(test_data,origin_budget)
    print("最终的长度：",len(test_data))

    for d in test_data:
        f.write(d+"\n")
    # f.write(str(len(test_data)))
    f.close()
    
    if len(test_data)<1:
        return (0,0,0)
    else :
        print(input+"  生成了target : "+str(len(test_data)))

    
    # do something for the seed region list,  i.e., patterns
    # Note the Outliers can be used for the next iter input
