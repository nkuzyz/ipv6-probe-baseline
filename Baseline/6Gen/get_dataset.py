tot_num = 100000
if __name__ =="__main__":
    a = open('../dataset1.txt')
    b = (a.readlines())
    a.close()
    print(len(b))
    c = open('./part_dataset.txt','w')
    result = []
    for i in b[:tot_num]:
        result.append(i.replace(':',''))
    c.write(''.join(result))
    c.close()