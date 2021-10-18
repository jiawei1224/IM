
# from NewIdea.IC import avgSize, runIC2, runIC
import random
import math
import copy
import networkx as nx
import time
import relatedtopicdegree
from Mar_Seven import Main_function
# from OldAL.DegreeDiscount import DegreeDiscountIC
from DiGraph import ReadFileConstructGraph
from IC1 import getICInfluence
# from OldAL.IMM import IMM

def EDV1(G, S, k):
    Ne = set()
    for i in range(0, k):
        neighbors = G.neighbors(S[i])  #获取S[i]的邻居顶点
        for j in neighbors:
            Ne.add(j)
    Ne = Ne - set(S)

    edv = k
    for u in Ne:
        other = 1
        Peu = G.predecessors(u)
        for v in Peu:
            if v in S:
                other *= 1-G[v][u]['weight']
        edv += 1-other
    return edv

def EDV(G, S, k):  #二跳EDV
    inf = k
    active_dict={}
    Ne=[]
    for i in range(0, k):
        neighbors1 = G.neighbors(S[i])  #获取S[i]的邻居顶点
        Ne.extend(neighbors1)
    Ne=set(Ne)-set(S)
    #一跳邻居顶点被激活的收益
    for u in Ne:
        other = 1
        Peu = G.predecessors(u)
        Can = set(Peu)&set(S)
        for v in Can:
            other *= 1-G[v][u]['weight']
        inf += (1-other)
        active_dict[u] = 1-other
    twohop_Ne = []
    #计算二跳邻居顶点
    for u in Ne:
        neighbors2 = G.neighbors(u)
        twohop_Ne.extend(neighbors2)
    twohop_Ne = set(twohop_Ne)-set(S)-Ne
    #二跳邻居顶点被激活的收益
    for u in twohop_Ne:
        other = 1
        Peu = G.predecessors(u)
        Can = set(Peu) & Ne
        for v in Can:
            other *= 1 - G[v][u]['weight']
        inf += (1 - other)*active_dict[v]
    return inf

def LS(G, A, k, Out_degree2, vlaue_num):
    num = 0
    while num <= 10:
        # print(A)
        avg1 = EDV1(G, A, k)
        old_A = copy.deepcopy(A)
        # 如果一直都没变化就直接跳出循环
        for u in range(0, len(A)):
            Su_neighbors = list(G.predecessors(A[u]))
            Su_neighbors = list(set(Su_neighbors) & set(Out_degree2.keys()))  # 将其中的出度小的节点直接忽略
            # print('邻居', len(Su_neighbors))
            Final_node = {}
            Final_active_node = []
            Active_One_node = []
            Active_Two_neighbor = []
            # print('邻居',len(Su_neighbors))
            if len(Su_neighbors) > vlaue_num:
                for u1 in Su_neighbors:  # 开始检索S节点的邻居节点被激活的节点的个数
                    # if float(Ep[(u1, A[u])]) >= random.random():
                    if float(G[u1][A[u]]['weight']) >= random.random():
                        Active_One_node.append(u1)
            elif(len(Su_neighbors) <= vlaue_num):
                Active_One_node.extend(Su_neighbors)
            # print('之后',len(Active_One_node))
            Final_active_node.extend(Active_One_node)
            # 寻找S种子集的邻居的邻居节点，如果存在多个节点激活一个节点的情况；
            for v in Active_One_node:
                neighbors = list(set(list(G.predecessors(v))) & set(Out_degree2.keys()))  # 后边可能需要改变
                # if len(neighbors) != 0:
                # print('邻居',len(neighbors))
                if len(neighbors) > vlaue_num:
                    for i in neighbors:
                        p = 1 - ((1 - float(G[v][A[u]]['weight'])) * (1 - float(G[i][v]['weight'])))
                        if p >= random.random():
                            Active_Two_neighbor.append(i)
                elif(len(neighbors) <= vlaue_num):
                     Active_Two_neighbor.extend(neighbors)
            Final_active_node.extend(Active_Two_neighbor)
            # 找根节点的前驱节点的前驱的前驱的前驱节点，其中已经找到二度前驱节点了，之后再根据第二各前驱节点再找其第三个前驱
            Active_Three_node = []
            for node in Active_Two_neighbor:
                predecessor_node = list(set(list(G.predecessors(node))) & set(Out_degree2.keys()))
                neighbors_Two = list(set(G.neighbors(node)) & set(Active_One_node))
                if len(predecessor_node) > vlaue_num:
                    for node_u in predecessor_node:
                        for node_v in neighbors_Two:
                            # p = 1 - ((1 - float(Ep[(node_u, node)])) * (1 - float(Ep[(node, node_v)])) * (
                            #             1 - float(Ep[node_v, A[u]])))
                            p = 1 - ((1 - float(G[node_u][node]['weight'])) * (1 - float(G[node][node_v]['weight'])) * (
                                    1 - float(G[node_v][A[u]]['weight'])))
                            if p >= random.random():
                                if node_u not in Active_Three_node:
                                    Active_Three_node.append(node_u)
                elif(len(predecessor_node) <= vlaue_num):
                    Active_Three_node.extend(predecessor_node)
            Final_active_node.extend(Active_Three_node)
            Final_active_node = list(set(Final_active_node))
            if len(Final_active_node) > 200:
                Final_active_node = random.sample(Final_active_node, 200)
            Snew = copy.deepcopy(A)
            for i in range(0, len(Final_active_node)):
                node = Final_active_node[i]
                A[u] = node
                Final_node[node] = EDV(G, A, k)  # 计算每个节点的
                # A = copy.deepcopy(Snew)
            # Final_node[A[u]] = avg1#这个不进行计算了，应该最终还是用不到
            Final_node[Snew[u]] = avg1
            final = dict(sorted(Final_node.items(), key=lambda v: v[1], reverse=True))
            if final[A[u]] < list(final.values())[0]:
                tm = list(final.keys())[0]
                if tm not in A:
                    A[u] = tm
        # 计算A'的最大影响力
        avg2 = EDV1(G, A, k)
        # avg2 = list(final.values())[0]#这个可以不用计算，直接可以使用，哈哈哈哈。
        # print(avg2,EDV(G,A,k))
        # count += 1
        Df = avg2 - avg1
        # print(Df)
        #必须通过循环找到一个符合条件的节点；
        if Df > 0:
            Snew = copy.deepcopy(A)
        # if len(set(Snew) & set(old_A)) == k:
        #     num += 1
        #     # print("计数器", num)
        #     if num >= 10:
        #         break
        # elif len(set(Snew) & set(old_A)) != k:
        #     num = 0
        # A = copy.deepcopy(Snew)
        # print('节点', u)
        if u!=k:
            break
    return Snew

