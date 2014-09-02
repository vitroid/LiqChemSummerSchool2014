#!/usr/bin/env python
# coding: utf-8



############# functions ###############################################
import invariants as inv
import distance_matrix as dm

def is_isomorphic(graphA, graphB):

    #local function for recursion
    def submatch(orderB):
        #現在照合しているノードの個数
        size = len(orderB)
        for i in range(size):
            #距離行列の、size番目の行がすべて一致するかどうかをチェックする
            if dmA[orderA[size-1]][orderA[i]] != dmB[orderB[size-1]][orderB[i]]:
                #一致しない場合はフラグを立ててループを脱出する
                return False
        #もし1行全部一致したら
        #ノード数がテンプレートのノード数に達していたら
        if size == len(dmB):
            #完全に一致した!
            return True
        else:
            #境界を拡張する。
            #orderBに含まれる頂点に隣接する頂点の集合を作る。
            neighbors = set()
            for v in orderB:
                #集合演算で簡単!
                neighbors |= set(graphB[v])
            #すでにorderBに含まれている頂点は除く
            neighbors -= set(orderB)
            #隣接頂点のなかから1つ選んでorderBを拡張し、再度マッチングを繰り返す
            subresult = []
            for v in neighbors:
                if submatch(orderB + [v,]):
                    return True
            return False

    #頂点の探索順序を定める。n番目の頂点はn-1番目までのグラフに連結になるように。
    def progressive_order(graph):
        orderB = [0]
        for loop in range(len(graph)-1):
            #orderBに含まれる頂点に隣接する頂点の集合を作る。
            neighbors = set()
            for v in orderB:
                #集合演算で簡単!
                neighbors |= set(graph[v])
                #すでにorderBに含まれている頂点は除く
                neighbors -= set(orderB)
            v = list(neighbors)[0]
            orderB.append(v)
        return orderB

    #予備チェック。不変量が一致しなければisomorphicではない。
    different = False
    for func in (inv.number_of_vertices, inv.number_of_edges,
                 inv.order_histogram,    inv.cycle_histogram):
        if func(graphA) != func(graphB):
            different = True
            break
    if different:
        return False
    #graph A側の探索順序は固定しておく。
    orderA = progressive_order(graphA)

    #あらかじめ距離行列を計算しておく(隣接行列でも可)
    dmA = dm.distance_matrix(graphA)
    dmB = dm.distance_matrix(graphB)
        
    #graph Bの頂点をひとつずつ始点とする
    #結果が判明すれば探索は随時打ち切る。(subgraph_isomorphismとは違う挙動)
    for v in range(len(graphB)):
        orderB = [v,]
        if submatch(orderB):
            return True
    return False
    
############# end of functions ########################################


        
#test case
if __name__ == "__main__":
    #グラフは、辺の集合(set)で表現する。
    #頂点のラベルは0からの連番とする。
    #辺は無向とし、2頂点のラベル(小さい順)のタプルで表す。

    #大きなグラフ(立方体グラフ)
    A_edges = set([(0,1),(1,2),(2,3),(0,3),
                        (0,4),(1,5),(2,6),(3,7),
                        (4,5),(5,6),(6,7),(4,7)])
    A_size = 8
    #小さなグラフ(四角形グラフ)
    #連結でなければならない。
    #なおかつ、n+1番目の頂点が、n番目までの頂点の作るグラフに連結でなければならない。
    B_edges = set([(0,1),(1,2),(2,3),(0,3)])
    B_size = 4

    C_edges = set([(0,1),(1,3),(2,3),(0,2)])
    C_size = 4

    #連結な頂点から頂点へたどっていきやすいように、隣接関係をリストで表現する。
    A_graph = dm.adjacency_table(A_edges, A_size)
    B_graph = dm.adjacency_table(B_edges, B_size)
    C_graph = dm.adjacency_table(C_edges, C_size)

    #マッチング
    #assume both graphs are connected graphs
    print "A==B?",is_isomorphic(B_graph, A_graph)
    print "A==C?",is_isomorphic(A_graph, C_graph)
    print "B==C?",is_isomorphic(B_graph, C_graph)

