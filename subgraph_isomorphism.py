#!/usr/bin/env python
# coding: utf-8

############# functions ###############################################
def submatch(template_dm, target_graph, target_dm, match_list):
    matched = True
    #現在照合しているノードの個数
    size = len(match_list)
    for i in range(size):
        v = match_list[i]
        #距離行列の、size番目の行がすべて一致するかどうかをチェックする
        if template_dm[size-1][i] != target_dm[match_list[-1]][v]:
            #一致しない場合はフラグを立ててループを脱出する
            matched = False
            break
    #もし1行全部一致したら
    if matched:
        #ノード数がテンプレートのノード数に達していたら
        if size == len(template_dm):
            #完全に一致した!
            print match_list
        else:
            #境界を拡張する。
            #match_listに含まれる頂点に隣接する頂点の集合を作る。
            neighbors = set()
            for v in match_list:
                #集合演算で簡単!
                neighbors |= set(target_graph[v])
            #すでにmatch_listに含まれている頂点は除く
            neighbors -= set(match_list)
            #隣接頂点のなかから1つ選んでmatch_listを拡張し、再度マッチングを繰り返す
            for v in neighbors:
                submatch(template_dm, target_graph, target_dm, match_list + [v,])
############# end of functions ########################################


from distance_matrix import *
        
#test case
if __name__ == "__main__":
    #グラフは、辺の集合(set)で表現する。
    #頂点のラベルは0からの連番とする。
    #辺は無向とし、2頂点のラベル(小さい順)のタプルで表す。

    #大きなグラフ(立方体グラフ)
    target_edges = set([(0,1),(1,2),(2,3),(0,3),
                        (0,4),(1,5),(2,6),(3,7),
                        (4,5),(5,6),(6,7),(7,4)])
    target_size = 8
    #小さなグラフ(四角形グラフ)
    #連結でなければならない。
    #なおかつ、n+1番目の頂点が、n番目までの頂点の作るグラフに連結でなければならない。
    template_edges = set([(0,1),(1,2),(2,3),(0,3)])
    template_size = 4

    #連結な頂点から頂点へたどっていきやすいように、隣接関係をリストで表現する。
    target_graph   = adjacency_table(target_edges,   target_size)
    template_graph = adjacency_table(template_edges, template_size)
    #距離行列を作る
    target_dm   = distance_matrix(target_graph)
    template_dm = distance_matrix(template_graph)

    #マッチング開始
    #targetの頂点をひとつずつ始点とする
    for v in range(target_size):
        match_list = [v,]
        submatch(template_dm, target_graph, target_dm, match_list)

#テンプレートグラフの対称性が高いと、同じsubgraphに何度もマッチする。
#重複は別のプログラムで除去する。