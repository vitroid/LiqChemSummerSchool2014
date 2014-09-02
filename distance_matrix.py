#!/usr/bin/env python
# coding: utf-8


############# functions ###############################################
#Dijkstra's shortest path algorithm with priority queue (modified from Wikipedia)

def Dijkstra(Graph, source):
    queue = set()
    size  = len(Graph)
    infinity = size
    undefined = None
    dist     = [0] * size
    dist[source]  = 0                     # Distance from source to source
    for v in range(size):                       # Initializations
        if not v == source:
            dist[v]     = infinity           # Unknown distance function from source to v
        queue.add(v)                         # All nodes initially in Q
 
    while len(queue) > 0:                  # The main loop
        u = -1
        dmin = infinity+1
        for i in queue:
            if dist[i] < dmin:
                dmin = dist[i]
                u    = i        # Source node in first case
        queue.remove(u)
        for v in Graph[u]:           # where v has not yet been removed from Q.
            alt = dist[u] + 1      #重みはいつも1
            if alt < dist[v]:               # A shorter path to v has been found
                dist[v]     = alt 
    #非連結な頂点間の距離を、-1にする。
    for i in range(size):
        if dist[i] == size:
            dist[i] = -1
    return dist


#辺の集合から、隣接関係に変換する。このほうがあとあと使いやすい。
def adjacency_table(edges,size):
    graph = [[] for i in range(size)]
    for edge in edges:
        i,j = edge
        graph[i].append(j)
        graph[j].append(i)
    #すべてタプルにする。(あとで使いやすいように)
    for i in range(size):
        graph[i] = tuple(graph[i])
    return tuple(graph)


#隣接関係をつかって距離行列を生成する
def distance_matrix(graph):
    dm = []
    for i in range(len(graph)):
        dm.append(Dijkstra(graph,i))
    return dm


############# end of functions ########################################

#test case
if __name__ == "__main__":
    #グラフは、辺の集合(set)で表現する。
    #頂点のラベルは0からの連番とする。
    #辺は無向とし、2頂点のラベル(小さい順)のタプルで表す。

    #立方体グラフ+孤立した辺
    edges = set([(0,1),(1,2),(2,3),(0,3),
                 (0,4),(1,5),(2,6),(3,7),
                 (4,5),(5,6),(6,7),(4,7),(8,9)])
    size = 10   #頂点の数
    #連結な頂点から頂点へたどっていきやすいように、隣接関係をリストで表現する。
    graph   = adjacency_table(edges,size)
    #距離行列を作る
    dm      = distance_matrix(graph)
    print dm

