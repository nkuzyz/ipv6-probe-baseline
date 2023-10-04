import re

def trans(pattern,budget_sample):
    with open(pattern,'r') as f:
        raw = f.readlines()
    f.close()
    expanded_addresses = []
    for i in raw[:-1]:
        ipv6_address = i.split(' ')[0]
        b = i.split(' ')[1]
        if(b.count('-')==0):
            ipv6_address = ipv6_address[1:]
            b = '0-'+b
        leng = ipv6_address.count('x')
        start_range = int(b.split('-')[0],16)
        end_range = int(b.split('-')[1],16)
        loc = ([substr.start() for substr in re.finditer('x', ipv6_address)])
        address_list = list(ipv6_address)
        for j in range(start_range,end_range):
            temp = (hex(j)[2:].zfill(leng))
            for k in range(leng):
                address_list[loc[k]]=temp[k]
            p = re.findall(".{4}",''.join(address_list))
            expanded_addresses.append(':'.join(p))
    expanded_addresses = list(set(expanded_addresses))
    with open(budget_sample,'w') as f:
        f.write('\n'.join(expanded_addresses))
    f.close()

trans