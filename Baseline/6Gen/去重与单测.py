import os,random
from ActiveScanD import scan_addr
def delete_repeat_ip(generate_samples,origin_samples):
    num = 2245000
    generate_samples = open('Baseline/6Gen/dataset2/{}/generate_samples.txt'.format(num),'r').readlines()
    origin_samples = open('Baseline/Database/dataset2.txt','r').readlines()

    generate_samples_set = set(generate_samples)
    origin_samples_set = set(origin_samples)

    generate_samples_set = generate_samples_set - origin_samples_set
    print(len(generate_samples_set))

    # sava generate_samples_set
    output = 'Baseline/6Gen/dataset2/{}/generate_samples_set.txt'.format(num)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    f = open(output, "w")
    for x in generate_samples_set:
        f.write(x)
    f.close()


def scan(sub_output,file):
    # scan and analysis
    
    result = []
    result.append([0,scan_addr(sub_output,file)])
    
    filename = sub_output+"/analydata.txt"
    os.makedirs(os.path.dirname(filename),exist_ok=True)
    w = open(filename,"a")
    for r in result:
        w.write("su_{}.txt : target {} , active {} , hit_rate {} \n".format(r[0],r[1][0],r[1][1],r[1][2]))

def hit_rate():
    dataset = 'Baseline/6Gen/dataset2/'
    num = 44900
    sub_output = dataset+'{}'.format(num)
    
    # generate_samples = open(sub_output+'/generate_samples_set.txt','r').readlines()
    # scan(sub_output,sub_output+'/generate_samples_set.txt')
    
    # if len(generate_samples) > num:
    #     generate_samples_random = random.sample(generate_samples,num)
    
    # # save generate_samples
    # output = sub_output+'/generate_samples.txt'
    # os.makedirs(os.path.dirname(output), exist_ok=True)
    # f = open(output, "w")
    # for x in generate_samples_random:
    #     f.write(x)
    # f.close()

    scan(sub_output,sub_output+'/generate_samples_unique.txt')

hit_rate()
# delete_repeat_ip('','')

