#!/usr/bin/env python
# coding: utf-8



############# functions ###############################################
def number_of_vertices(graph):
    return len(graph)

#有向か無向かを判別しないので、無向グラフでは辺の本数が倍になる。
def number_of_edges(graph):
    noe = 0
    for neighbor_list in graph:
        noe += len(neighbor_list)
    return noe

#histogram of vertex orders
def order_histogram(graph):
    orders = [len(neighbor_list) for neighbor_list in graph]
    maxo = max(orders)
    histogram = [0 for i in range(maxo+1)]
    for i in orders:
        histogram[i] += 1
    return tuple(histogram)


from cycles import unique_cycles

#histogram of cycle size
def cycle_histogram(graph,maxc=6):
    cycles = unique_cycles(graph,maxc)
    cycle_size = [len(cycle) for cycle in cycles]
    histogram = [0 for i in range(maxc+1)]
    for cs in cycle_size:
        histogram[cs] += 1
    return tuple(histogram)

    
############# end of functions ########################################

from distance_matrix import *

#test case
if __name__ == "__main__":
    #グラフは、辺の集合(set)で表現する。
    #頂点のラベルは0からの連番とする。
    #辺は無向とし、2頂点のラベル(小さい順)のタプルで表す。

    #大きなグラフ(立方体グラフ)
    edges = set([(0,1),(1,2),(2,3),(0,3),
                        (0,4),(1,5),(2,6),(3,7),
                        (4,5),(5,6),(6,7),(7,4)])
    size = 8

    #連結な頂点から頂点へたどっていきやすいように、隣接関係をリストで表現する。
    graph   = adjacency_table(edges, size)
    #頂点の個数
    print number_of_vertices(graph)
    #辺の本数
    print number_of_edges(graph)
    #次数のヒストグラム
    print order_histogram(graph)
    #cycleのヒストグラム
    print cycle_histogram(graph,6)
