import random


'''
根据模式生成ipv6地址,需要去重。
'''

def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]

def random_replace_givenum(list_temp,num):
    if num <=0 : return []
    seed = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    lists = [list_temp]*num
    for j in list_temp:
        if j=='*':
            replace_element = random.sample(seed*num,num)
            for i in range(num):
                lists[i]=lists[i].replace(j,replace_element[i],1)
    return lists


def random_replace(list_temp,num):
    if num <=0 : return []
    seed = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    lists = [list_temp]
    for j in list_temp:
        if j=='*':
            replace_element = random.sample(seed,num)
            temps = lists
            lists = []
            for x in temps:
                x = [x] * num
                for i in range(num):
                    x[i]=x[i].replace(j,replace_element[i],1)
                lists+=x
    return lists






def random_gernerate(modules,samples,budget):
    single_pattern_budget = (int(budget/len(modules))+1)
    test_data=[]
    new_modules = []
    new_samples = []
    flag = 0
    if(len(modules)>budget):
        flag = 1
        sam_num = random.sample(range(len(modules)),budget)
        for m in range(len(modules)):
            if m in sam_num:
                print(m)
                new_modules.append(modules[m])
                new_samples.append(samples[m])
    else :
        new_modules = modules
        new_samples = samples

    
    for m in range(len(new_modules)):
        unique_samples = set(new_samples[m])
        c = new_modules[m].count('*')

        generate_samples = []
        if single_pattern_budget > pow(16,c)-len(unique_samples):
            generate_samples=set(random_replace(new_modules[m],16))
        else:
            if flag == 1:
                generate_samples=set(random_replace_givenum(new_modules[m],(single_pattern_budget+len(unique_samples))*2))
            else:
                generate_samples=set(random_replace_givenum(new_modules[m],(single_pattern_budget+len(unique_samples))*10))

                # x = 1
                # while pow(x,c)<single_pattern_budget+len(unique_samples) : x+=1
                # if x>16 : x =16 
                # else : x = x
                
                # if(pow(x,c)>budget):
                #     generate_samples=set(random_replace(new_modules[m],x-1))
                # else:
                #     generate_samples=set(random_replace(new_modules[m],x))
        


        generate_samples = generate_samples-unique_samples
        unique_samples = generate_samples | unique_samples
        print('6Graph     '+str(len(generate_samples))+"/"+ str(single_pattern_budget))
        format_data = []
        for x in generate_samples:
            # print(x)
            temp = ":".join(cut(x,4))
            format_data.append(temp)
        test_data.append(format_data)
    return test_data







# 定义字符串
# str = "200113882f0e0000*****00*********"

# print(random_replace_givenum(str,18))

# # 定义生成字符串的数量
# num_strings = 100

# # 循环生成字符串
# for i in range(num_strings):
#     # 将星号替换成随机数字
#     new_str = str.replace("*", str(random.randint(0, 9)), 2)
#     new_str = new_str.replace("*", str(random.randint(0, 9)), 1)
    
#     # 输出新字符串
#     print(new_str)