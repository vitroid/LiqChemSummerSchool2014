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
def order_hist(graph):
    orders = [len(neighbor_list) for neighbor_list in graph]
    maxo = max(orders)
    hist = [0 for i in range(maxo+1)]
    for i in orders:
        hist[i] += 1
    return tuple(hist)

#(reducible) cycles
def reducible_cycles(graph, maxc=6):

    def self_avoiding_walk(graph,vertex_list):
        #迷走して経路長が長くなりすぎた時は
        if len(vertex_list) == maxc+1:
            #あきらめる。(結果なし)
            return []
        last = vertex_list[-1]
        results = []
        #last頂点に隣接する頂点それぞれについて
        for next in graph[last]:
            #もしnextが経路の最初の頂点に戻ってきて、しかも経路長が3以上なら、
            if next == vertex_list[0] and len(vertex_list) >= 3:
                #帰ってきた!
                #vertex_listを、結果に加える
                results.append(vertex_list)
            #自己回避経路(self-avoiding walk)になっているなら
            elif not next in vertex_list:
                #再帰的にwalkを延ばす
                results += self_avoiding_walk(graph,vertex_list + [next,])
        return results        
                
    cycles = []
    graph_size = len(graph)
    #すべての頂点を順番に始点として、
    for v in range(graph_size):
        #self-avoiding pathをさがす
        cycles += self_avoiding_walk(graph, [v,])
    #重複するサイクルを省く。(始点が違うだけ、逆回りなどすべて)
    #重複のないリスト
    uniquecycles = []
    #重複のない集合
    uniqueset = set()
    for cycle in cycles:
        #cycleに含まれる頂点を集合にする。
        fs = frozenset(cycle)
        #その集合が、既出でなければ
        if not fs in uniqueset:
            #集合の集合に追加する
            uniqueset.add(fs)
            #リストにも追加する
            uniquecycles.append(cycle)
    #リストのほうを返り値とする
    return uniquecycles

def cycle_hist(graph,maxc=6):
    cycles = reducible_cycles(graph,maxc)
    cycle_size = [len(cycle) for cycle in cycles]
    hist = [0 for i in range(maxc+1)]
    for cs in cycle_size:
        hist[cs] += 1
    return tuple(hist)

    
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
    graph   = adjacency_table(edges,   size)
    #頂点の個数
    print number_of_vertices(graph)
    #辺の本数
    print number_of_edges(graph)
    #次数のヒストグラム
    print order_hist(graph)
    #cycleのヒストグラム
    print cycle_hist(graph,6)
