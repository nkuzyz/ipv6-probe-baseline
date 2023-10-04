import matplotlib.pyplot as plt

def str2timestamp(s):
    t_stamp = 0
    s = s.split(",")
    if len(s) == 2:
        t_stamp += int(s[0].split(" ")[0]) * 86400
        s = s[1]
    else:
        s = s[0]
    s = list(map(int, s.split(".")[0].split(":")))
    t_stamp += s[0] * 3600 + s[1] * 60 + s[2]
    return t_stamp

consumes = list()
hits = list()
intimes = list()

with open("progress.txt", "r") as fin:
    for line in fin.readlines():
        if len(line) == 0:
            continue
        consumehit_intime = line.split(" in ")
        intime = consumehit_intime[1]
        consume_hit = consumehit_intime[0].split(" hit ")

        consume = int(consume_hit[0].split("consume ")[1])
        hit = int(consume_hit[1])
        intime = str2timestamp(intime)
        consumes.append(consume)
        hits.append(hit)
        intimes.append(intime)

pre_consumes = [0]
pre_consumes.extend(consumes[:-1])
per_consumes = [consumes[i] - pre_consumes[i] for i in range(len(consumes))]
pre_hits = [0]
pre_hits.extend(hits[:-1])
per_hits = [hits[i] - pre_hits[i] for i in range(len(hits))]
hit_rates = [per_hits[i] / per_consumes[i] for i in range(len(hits))]

plt.plot(intimes, hits, markerfacecolor='blue',marker='+')
plt.xlabel('time/s')
plt.ylabel('generated addresses')
plt.title('Cumulative number of generated addresses')
plt.grid()
# plt.show()
plt.savefig("Cumulative number of generated addresses.png")
plt.close()
plt.plot(range(1, len(hit_rates)+1), hit_rates, markerfacecolor='blue',marker='+')
plt.xlabel('iterations')
plt.ylabel('hit rate')
plt.title('Hit rates (per iteration will consume about 20000 probes)')
plt.grid()
# plt.show()
plt.savefig("Hit rates.png")
plt.close()
    