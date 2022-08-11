# © <2022> The University of Leeds and Yajie Sun
import igraph
from igraph import *
from copy import deepcopy

MULTISET = 'curr_multiset'
PREV_LABEL = 'l_previous'
CURRENT_LABEL_STR = 's_current'


class LabelCompression:
    def __init__(self):
        self.HASH = dict()
        self.HASH['index'] = '0'

    def getHASH(self):
        return self.HASH

    def createTestGraph(self):
        testGraph = Graph.GRG(10, 0.2)
        i = 1
        for v in testGraph.vs:
            v[CURRENT_LABEL_STR] = str(i % 3 + 1)
            i = i + 1
        testGraph['name'] = 'LGtest'
        return testGraph

    def compress(self, g):
        labels = []
        # new_labels = [v[MULTISET] for v in g.vs]
        labels = [v[CURRENT_LABEL_STR] for v in g.vs]
        labels.sort()
        for s in labels:
            fs = -1
            if s not in self.HASH:
                currentIndex = self.HASH['index']
                newIndex = str(int(currentIndex) + 1)
                self.HASH['index'] = newIndex
                fs = newIndex
                self.HASH[s] = fs
        # relabelling
        for v in g.vs:
            v[PREV_LABEL] = self.HASH[v[CURRENT_LABEL_STR]]
        g.set_of_newly_created_labels = set([v[PREV_LABEL] for v in g.vs])
        return g

    def testGraph(self):
        return self.testGraph


class Weisfeiler_Lehman:
    def init_iteration(selcf, g):
        for v in g.vs:
            v[CURRENT_LABEL_STR] = v[PREV_LABEL] = str(v.degree())

    def execute(self, g1, g2, num_of_iterations):
        compressor = LabelCompression()

        self.init_iteration(g1)
        self.init_iteration(g2)

        g1 = compressor.compress(g1)  # hash initialization
        g2 = compressor.compress(g2)  # hash initialization
        # print(str(compressor.getHASH()))
        ret = True
        for index in range(1, num_of_iterations):
            generate_labels(g1)
            generate_labels(g2)
            generate_string_labels(g1)
            generate_string_labels(g2)

            g1 = compressor.compress(g1)
            g2 = compressor.compress(g2)
            # compare g1 and g2
            # print(str(compressor.getHASH()))
            # print(g1.setOfNewlyCreatedLabels)
            # print(g2.setOfNewlyCreatedLabels)
            # aaa = [v[MULTISET] for v in g1.vs]
            if g1.set_of_newly_created_labels == g2.set_of_newly_created_labels:
                pass
            else:
                print("Iter#" + str(index) + ": Labels mismatch")
                ret = False
                break
        return ret


def generate_labels(g):
    for v in g.vs:
        v[MULTISET] = []
        for nv in v.neighbors():
            v[MULTISET].append(nv[PREV_LABEL])
        v[MULTISET].sort()


def generate_string_labels(g):
    for v in g.vs:
        concatString = ""
        for each in v[MULTISET]:
            concatString = concatString + str(each)
        v[CURRENT_LABEL_STR] = str(v[PREV_LABEL]) + concatString


def generateTree(nodes, seed):
    degree = seed
    g = Graph.Tree(nodes, degree)
    return g


def generateRandom(seed):
    prob = seed
    g = Graph.GRG(10, prob)
    return g


def displayG(g):
    layout = g.layout("kk")
    plot(g, layout=layout,
         vertex_label=g.vs.indices, edge_width=[2], vertex_color=['green'],
         edge_color=['black'])


def display_str_G(g):
    new_vs = list()
    v_names = g.vs.indices
    for idx, v in enumerate(g.vs):
        s_current = v[CURRENT_LABEL_STR]
        v_name = v_names[idx]
        new_vs.append(str(v_name) + "_" + s_current)
    layout = g.layout("kk")
    plot(g, layout=layout,
         vertex_label=new_vs, edge_width=[2], vertex_color=['green'],
         edge_color=['black'])


if __name__ == '__main__':
    # 构建第一个图
    g1 = igraph.Graph()
    g1.add_vertices(6)
    g1.add_edges([(0, 3), (3, 4), (1, 4), (1, 2), (2, 4), (2, 3), (3, 5)])

    g2 = igraph.Graph()
    g2.add_vertices(6)
    g2.add_edges([(0, 3), (1, 3), (1, 4), (2, 4), (2, 5), (2, 3), (3, 4)])
    displayG(g1)
    displayG(g2)

    n = 12
    wl_alg = Weisfeiler_Lehman()
    g1['name'] = 'G1'
    g2['name'] = 'G2'
    # displayG(G1)
    isomorphic = wl_alg.execute(g1, g2, n)

    # 显示网络情况
    display_str_G(g1)
    display_str_G(g2)
    print("Is it graph-isomorphic? " + str(isomorphic))
