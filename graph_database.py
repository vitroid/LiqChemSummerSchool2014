#!/usr/bin/env python
# coding: utf-8



############# functions ###############################################
import isomorphism as im
import invariants as inv

#idを調べて返す。
def graph_query(graph, db, lst, add=False):
    invar = (inv.number_of_vertices(graph), inv.number_of_edges(graph),
             inv.order_histogram(graph), inv.cycle_histogram(graph,6))
    #既存の、同じinvariantを持つグラフのリストを入手
    if db.has_key(invar):
        candidates = db[invar]
        found = False
        for id in candidates:
            if im.is_isomorphic(graph, lst[id]):
                return id
    else:
        db[invar] = []
    #見付からない場合
    #addしても構わないなら
    if add:
        #id->graph対応表に追加
        lst.append(graph)
        #id決まる。
        id = len(lst)-1
        #graph->id対応表に追加
        db[invar].append(id)
        #idを返す
        return id
    return -1

#実際の運用では、DB全体を保存したり読みこんだりする機能がないと、使いづらいだろう。


############# end of functions ########################################

import distance_matrix as dm

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

    B_edges = set([(0,1),(1,2),(2,3),(0,3)])
    B_size = 4

    #連結な頂点から頂点へたどっていきやすいように、隣接関係をリストで表現する。
    graph   = dm.adjacency_table(edges,   size)
    B       = dm.adjacency_table(B_edges,   B_size)

    #データベースとは辞書である。
    #今回の場合、キーにはいくつかの不変量を
    #値には同じ不変量をもつグラフの通し番号のリストを格納する。
    #グラフそのものは別のリストに蓄える。
    #データベースは、尋ねられたグラフの通し番号を与えるのみ。
    #個数を数えたりするのは、その通し番号を使って別途行えばいい。
    #データベースの機能は最小限にする。

    #グラフ辞書; グラフの形からIDを調べるのに使用
    graph_db = dict()
    #既知のグラフの配列; グラフのIDから形を調べるのに使用
    graph_list = []
    
    print graph_query(graph, graph_db, graph_list, add=False) #登録されていないので-1
    print graph_query(graph, graph_db, graph_list, add=True)  #0番として登録
    print graph_query(graph, graph_db, graph_list, add=False) #0番で登録済み
    print graph_query(B, graph_db, graph_list, add=False) #登録されていないので-1
    print graph_query(B, graph_db, graph_list, add=True)  #1番として登録
    print graph_query(B, graph_db, graph_list, add=False) #1番で登録済み
    print graph_query(graph, graph_db, graph_list, add=True)  #0番で登録済み
