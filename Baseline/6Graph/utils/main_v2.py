from Graph import Start
import sys,os,re,time

# file_path = 'DET/det_output.txt'
# os.makedirs(os.path.dirname(file_path), mode=777,exist_ok=True)

print("我开始啦")

# sys.stdout = open(file_path, "w")

# f = open("few_test_prefix_list.txt","r")

# prefixs = eval(f.readline())


budget = [100*500,1000*500,10000*500]

for b in budget:
    result = []
    times = time.asctime().replace(' ','_')
    # for p in prefixs:
    # # p=prefixs[0]
    # # p = 4843
    #     input = "data/few_"+str(p)
    #     output = "6Graph/output_"+str(budget)+"/few_"+str(p)
    #     result.append([p,Start(input,output,budget)])
    # input = "Baseline/Database/su_seed_463"
    input = '/home/chengdaguo/ipv6/Baseline/Database/few_data_500.txt'
    output = "Baseline/6Graph/output_su/output_"+str(b)+"/total_"+str(times)
    result.append([0,Start(input,output,b)])

    filename = "Baseline/6Graph/output_su/output_"+str(b)+"/total"+str(times)+"/analydata.txt"
    os.makedirs(os.path.dirname(filename),exist_ok=True)
    w = open(filename,"w")
    for r in result:
        w.write("few_{}.txt : target {} , active {} , hit_rate {} \n".format(r[0],r[1][0],r[1][1],r[1][2]))

    target_sum = 0
    active_sum = 0
    for r in result:
        target_sum+=r[1][0]
        active_sum+=r[1][1]

    if target_sum!=0: hit_rate_sum = active_sum/target_sum
    else :hit_rate_sum = 0
    w.write("sum : target {} , active {} , hit_rate {} \n".format(target_sum,active_sum,hit_rate_sum))
        

    w.close()