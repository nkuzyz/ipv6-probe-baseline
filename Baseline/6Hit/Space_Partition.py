import random

from _Definition import *
import itertools
import collections
import queue
from iteration_utilities import first


def initialize_root():
    return Node()


def create_node(f: Node, c: set, extra_dimension=None):
    node = Node()
    node.assigned_dimension = node.assigned_dimension.union(f.assigned_dimension)
    if extra_dimension is not None:
        node.assigned_dimension.add(extra_dimension)
    node.assigned_seed = node.assigned_seed.union(c)
    return node


def partition(c: set, d: int):
    sub_map = collections.defaultdict(set)
    for s in c:
        sub_map[s[d]].add(s)
    return sub_map.values()


def dhc(node: Node):
    if len(node.assigned_dimension) < 31:
        # for dimension in node.unassigned_dimension:
            # if all(ci[dimension] == cj[dimension] for ci, cj in itertools.combinations(node.assigned_seed, 2)):
                # 判断条件可以优化
                # node.assigned_dimension.add(dimension)
        node.add_assigned_dimension()
        dimension_star = None
        for i in range(1, 33):
            if i not in node.assigned_dimension:
                dimension_star = i
                break
        if dimension_star is not None:
            for sequence in partition(node.assigned_seed, dimension_star):
                new_node = create_node(node, sequence, extra_dimension=dimension_star)
                node.child_nodes.append(new_node)
            for child in node.child_nodes:
                dhc(child)


def add_r_nodes(root: Node):
    q = queue.Queue()
    q.put(root)
    while not q.empty():
        node = q.get()
        if len(node.child_nodes) > 0:
            assigned_value = collections.defaultdict(set)
            for child in node.child_nodes:
                q.put(child)
                for dimension in child.assigned_dimension.difference(node.assigned_dimension):
                    assigned_value[dimension].add(first(child.assigned_seed)[dimension])
            r_node = Node(assigned_value=assigned_value)
            r_node.assigned_dimension = node.assigned_dimension
            r_node.assigned_seed = node.assigned_seed
            node.child_nodes.append(r_node)


def init_partition(seeds_num=1000, file_name="responsive-addresses.txt", seeds=None) -> Node:
    if seeds is None:
        seeds = set()
        with open(file_name, "r") as fin:
            fin.readline()
            for net in fin.readlines():
                net = net.strip()
                if len(net) > 0:
                    seeds.add(Addr(net))
                    if len(seeds) > seeds_num:
                        break
        print(f"--- Initialised {len(seeds)} seed addresses")
    d0 = initialize_root()
    d1 = create_node(d0, seeds)
    d0.child_nodes.append(d1)
    print("--- The root node is done")
    dhc(d1)
    print("--- Adding R nodes")
    add_r_nodes(d0)
    return d0


def space_repartition(m: int, addr_pool, pc: float, pu: float) -> Node:
    def selection(a):
        return sample(a, 2)

    def crossover(a1, a2):
        if random.random() < pc:
            cs_point = random.randint(17, 32) - 1
            return (Addr(a1.to_hex()[0:cs_point] + a2.to_hex()[cs_point:]),
                    Addr(a2.to_hex()[0:cs_point] + a1.to_hex()[cs_point:]))
        else:
            return (Addr(a1.to_hex()), Addr(a2.to_hex()))



    def mutation(a):
        if random.random() < pu:
            mutation_point = random.randint(1, 16) - 1
            return Addr(a.to_hex()[0:mutation_point] + hex(random.randint(0, 15))[2:] + a.to_hex()[mutation_point + 1:])
        else:
            return Addr(a.to_hex())

    n = set()
    while len(n) <= m:
        ai, aj = selection(addr_pool)
        aic, ajc = crossover(ai, aj)
        aicm = mutation(aic)
        ajcm = mutation(ajc)
        n.add(aicm)
        n.add(ajcm)
    return init_partition(len(n), seeds=n)


if __name__ == '__main__':
    init_partition()
