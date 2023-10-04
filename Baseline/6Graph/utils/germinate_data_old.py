import random


'''
根据模式生成ipv6地址,需要去重。
'''

def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]

def random_replace(list_temp):
    seed = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    for j in list_temp:
        if j=='*':
            list_temp=list_temp.replace(j,random.choice(seed),1)
    return list_temp


def random_gernerate(modules,samples):
    test_data=[]
    gernerate_num = {1:5,2:10,3:15,4:20,5:30}
    for m in range(len(modules)):
        c = modules[m].count('*')
        if c > 5:
            t = 40
        elif c<1:
            t=0
        elif pow(16,c)-len(samples[m]) < gernerate_num[c]:
            t = pow(16,c)-len(samples[m])-2
        else:
            t = gernerate_num[c]
        i = 0
        while(i<t):
            x = random_replace(modules[m])
            # print(x)
            if x not in samples[m]:
                i+=1
                samples[m].append(x)
                temp = ":".join(cut(x,4))
                test_data.append(temp)
            
        
    return test_data








# # 定义字符串
# str = "200113882f0e0000*****00*********"

# # 定义生成字符串的数量
# num_strings = 100

# # 循环生成字符串
# for i in range(num_strings):
#     # 将星号替换成随机数字
#     new_str = str.replace("*", str(random.randint(0, 9)), 2)
#     new_str = new_str.replace("*", str(random.randint(0, 9)), 1)
    
#     # 输出新字符串
#     print(new_str)