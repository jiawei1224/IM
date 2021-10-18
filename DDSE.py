"""
DDSE 没有问题，可以放心使用
"""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import networkx as nx
import networkx as nt
from IC1 import getICInfluence
# from NetWork.LT import getLTInfluence
import random
import copy
import relatedtopicdegree
import time
from queue import Queue
# 以有向图的形式实现DDSE，因此在求EDV时，邻居顶点到S的边数少于无向图，导致EDV相比无向图稍小

# 将I赋值给M，并将M[i]按一定概率变异
def Mutation(G,I,vexlist,f,k,n):
    M=[]
    for i in range(0,n):
        Mi=copy.copy(I[i])
        # print(id(Mi))
        up_bound=k*(i+5)
        if(up_bound>len(G.nodes)):
            up_bound=len(G.nodes)
        for j in range(0,k):
            if random.random()<f:
                DDS=Degree_Descending_Search(G,vexlist,k,Mi)
                index = random.randint(0, up_bound-1)
                Mi[j]=DDS[index%k]
        M.append(Mi)
    return M
# 将M和I按一定概率重组生成C
def Crossover(G,M,I,vexlist,cr,k,n):
    C=[]
    for i in range(0,n):
        Ci=[]
        up_bound=k*(i+5)
        if(up_bound>len(G.nodes)):
            up_bound=len(G.nodes)
        for j in range(0,k):
            if random.random()<cr:
                node=M[i][j]
                while node in Ci:
                    DDS=Degree_Descending_Search(G,vexlist,k,Ci)
                    index=random.randint(0,up_bound-1)
                    node=DDS[index%k]
            else:
                node=I[i][j]
                while node in Ci:
                    DDS=Degree_Descending_Search(G,vexlist,k,Ci)
                    index = random.randint(0, up_bound-1)
                    node=DDS[index%k]
            # print(j,node)
            # 此时Ci中没有值，下标0是不存在的
            Ci.insert(j,node)
        C.append(copy.copy(Ci))
    # print(I)
    # print(M)
    # print(C)
    return C

def EDV(G,S,k):
    # print("S is {}".format(S))
    Ne=set()
    for i in range(0,k):
        neighbors=G.neighbors(S[i])  #获取S[i]的邻居顶点
        for j in neighbors:
            Ne.add(j)
    # print(Ne)
    Ne=Ne-set(S)
    edv=k
    # print("Ne is {}".format(Ne))
    for u in Ne:
        x=getLink(G,S,u)    #获取S中顶点指向u的边的数量   有向图
        # print("vex is {} and x is {}".format(u,x))
        # 无向图边数
        # neu=G.neighbors(u)
        # x=len(set(neu)&set(S))
        other=1
        Peu=G.predecessors(u)
        for v in Peu:
            if v in S:
                other*=1-G[v][u]['weight']
        edv+=1-other
    # print(edv)
    return edv

# 比较C[i]和I[i]的EDV，并选择较大的更新Selection
def Selection(G,C,I,k,n):
    Se=[]
    HighEDV=[]
    for i in range(0,n):
        # a=time.time()
        edvi=EDV(G,I[i],k)
        edvc=EDV(G,C[i],k)
        # b=time.time()
        # print(b-a)
        # print(I[i])
        # print(C[i])
        if edvi>edvc:
            Se.append(I[i])
            # print(Se)
            HighEDV.insert(i,edvi)
        else:
            Se.append(C[i])
            # print(Se)
            HighEDV.insert(i,edvc)
    return Se,HighEDV

# 以S[i]的邻居顶点替换S[i]得到St，EDV大的作为S
def LocalSearch(G,S,k):
    edv=0
    for u in S:
        neighbors=G.neighbors(u)
        index=S.index(u)
        for v in neighbors:
            if v not in S:
                St=copy.copy(S)
                St[index]=v
                edvs=EDV(G,S,k)
                edvst=EDV(G,St,k)
                if edvst>edvs:
                    S=St
                    edv=edvst
                else:
                    edv=edvs
    return S,edv


