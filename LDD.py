''' Implementation of degree discount heuristic [1] for Independent Cascade model1
of influence propagation in graph G
[1] -- Wei Chen et al. Efficient influence maximization in Social Networks (algorithm 4)
'''
__author__ = 'ivanovsergey'
from priorityQueue import PriorityQueue as PQ  # priority queue
import relatedtopicdegree
import networkx as nx
def LDD(G, k, p):
    ''' Finds initial set of nodes to propagate in Independent Cascade model1 (with priority queue)
    Input: G -- networkx graph object
    k -- number of nodes needed
    p -- propagation probability
    Output:
    S -- chosen k nodes
    '''
    # p = dict()
    # read in graph

    tp = relatedtopicdegree.readdata()
    S = []
    dd = PQ()  # degree discount
    t = dict()  # number of adjacent vertices that are in S
    d = dict()  # degree of each vertex
    r=dict()
    pf = dict()
    # initialize degree discount
    for u in G.nodes():
        d[u] = 0
        for v in G[u]:
            if tp[v]==1:
               d[u] = d[u]+1  # each edge adds degree 1
        # d[u] = len(G[u]) # each neighbor adds degree 1
        dd.add_task(u, -d[u])  # add degree of each node
        t[u] = 0
        r[u]=0
        pf[u] = 0
    # add vertices to S greedily
    for i in range(k):
        u, priority = dd.pop_item()  # extract node with maximal degree discount
        S.append(u)
        for v in G[u]:

            for l in G[v]:
                if tp[l] != 1:
                    pf[v] += tp[l] * float(p[v, l])
            if v not in S:
                t[v] += G[u][v]['weight']  # increase number of selected neighbors
                if tp[u]==1:
                    r[v]+=G[u][v]['weight']
                # priority = d[v] - 2 * t[v] - (d[v] - t[v]) * t[v] * (p[u,v])  # discount of degree
                # priority = d[v]-2 * t[v]-(d[v]-t[v]) * t[v] * float(p[u,v])

                priority = ((1-float(p[u,v]))**(t[v]+r[v]))*(1+pf[v])
                dd.add_task(v, -priority)
    # print(S)
    return S


