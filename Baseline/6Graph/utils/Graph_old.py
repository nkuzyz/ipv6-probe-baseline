
from SpacePartition import *
from PatternMining import *
from germinate_data_new import random_gernerate
import sys
import os,random
from convert import convert
from reference.ActiveScan import scan_addr
 
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
    pattern_module =[]
    pattern_sample =[]
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
        pattern_module.append("".join(address_space))
        # print("-"*32)
        samples=[]
        for iparr in p:
            # print("".join([format(x, "x") for x in iparr]))
            samples.append("".join([format(x, "x") for x in iparr]))
        pattern_sample.append(samples)
        # print()


    print("正式的找模式  算法完成，接下来打印数据然后生成数据的步骤开始了！！！！！！！")
    f1 = open(filename+'ordinary_patterns.txt', "w")    
    sys.stdout = f1
    for m in pattern_module:
        print(m)
    print(len(pattern_module))


    f2 = open(filename+'ordinary_samples.txt',"w")
    sys.stdout = f2
    f1.close()
    for s in pattern_sample:
        print(s)
    print(len(pattern_sample))
 
    # sys.stdout = open(filename+'generate_samples.txt',"w")
    # f2.close()


    # test_data = []
    # test_data = random_gernerate(pattern_module,pattern_sample)
    # for d in test_data:
    #     print(d)
    # print(len(test_data))

        # show_regions(p)
    # print(len(pattern_module))
    # print(len(pattern_sample))
    # print(len(test_data))



def Start(input,output,budget):
    
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
    pattern_module =[]
    pattern_sample =[]
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
        pattern_module.append("".join(address_space))
        # print("-"*32)
        samples=[]
        for iparr in p:
            # print("".join([format(x, "x") for x in iparr]))
            samples.append("".join([format(x, "x") for x in iparr]))
        pattern_sample.append(samples)
        # print()

    

    # print(patterns_count)
    f1 = open(output+'/ordinary_patterns.txt', "w")    
    # f1.write("real pattern_count: "+str(patterns_count)+'\n')
    for m in pattern_module:
        f1.write(m+'\n')
    f1.close()

    # f2 = open(output+'/ordinary_samples.txt',"w")
    # sys.stdout = f2
    # print(len(pattern_sample))
    # for s in pattern_sample:
    #     print(s)
    # f2.close()

    f = open(output+'/generate_samples.txt',"w")
    
    test_data=set()
    single_pattern_budget = (budget/len(pattern_module)+1)*2
    # test_data = random_gernerate(pattern_module,pattern_sample,single_pattern_budget)
    # if len(test_data) > budget:
    #     test_data = random.sample(test_data,budget)
    test_data_origin = random_gernerate(pattern_module,pattern_sample,budget)

    test_data_more = []
    for t in test_data_origin:
        if(len(t)<single_pattern_budget):
            test_data = test_data|set(t)
        else :
            test_data_more.append(t)
    
    x = len(test_data_more)

    test_data_more = num_sort(test_data_more)
    
    for t in range(len(test_data_more)):
        
        if x == 1:
            rest = int ((budget - len(test_data))/x)
        else :
            rest = int ((budget - len(test_data))/x)+1

        if(rest>=len(test_data_more[t])):
            test_data |= set(test_data_more[t])
            x = x-1
        else :
            
            test_data |= set(random.sample(test_data_more[t],rest))
            x = x-1



    for d in test_data:
        f.write(d+"\n")
    # f.write(str(len(test_data)))
    f.close()
    
    if len(test_data)<1:
        return (0,0,0)
    else :
        print(input+"  生成了target : "+str(len(test_data)))
        return scan_addr(output,output+'/generate_samples.txt')
    
    # do something for the seed region list,  i.e., patterns
    # Note the Outliers can be used for the next iter input
