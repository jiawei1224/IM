"""
基于DE的IM算法
使用二跳EDV作为评估标准
"""
import copy,time,math
import random
from DiGraph import ReadFileConstructGraph
from IC1 import getICInfluence
from random import sample
import relatedtopicdegree
import heapq
from priorityQueue import PriorityQueue as PQ


def LocalInfluence(G, dictonehop, v):
    Nev = G.neighbors(v)
    localInfluence = 1
    for u in Nev:
        # Neu=G.neighbors(u)
        # Interset=set(Nev)&set(Neu)
        # for p in Interset:
        #     localInfluence-=1-(1-G[v][p]['weight'])*(1-G[v][u]['weight']*G[u][p]['weight'])
        localInfluence += G[v][u]['weight'] + G[v][u]['weight'] * dictonehop[u]
    return localInfluence

def Influence_Descending_Sort(G):
    node_inf = {}
    onehopinf={}
    for v in G.nodes:
        onehopinf[v]=onehopInfluence(G,v)
    for v in G.nodes:
        node_inf[v] = LocalInfluence(G,onehopinf,v)  # 需要测试使用哪种度的效果更好
    nodelist = sorted(node_inf.items(), key=lambda x: x[1], reverse=True)
    # print(nodelist)
    return nodelist,node_inf

def LID_Search(nodelist,k,eta,theta):
    N=[]
    listlen=len(nodelist)
    for i in range(k):
        up_bound=eta*i+theta  #已修改，论文也需要对应修改10*(i+5)
        if up_bound>listlen:
            up_bound=listlen
        node=nodelist[random.randint(0,up_bound-1)][0]
        while node in N:
            node = nodelist[random.randint(0, up_bound - 1)][0]
        N.append(node)
    return N


def singleMutation(Xr,Can_set,nodelist,node_inf,F,k,eta,theta):
    Mi=copy.copy(Xr)
    Can_set_num=len(Can_set)
    N=int(F*Can_set_num)
    Midict = {}
    for u in Mi:
        Midict[u] = node_inf[u]
    list = sorted(Midict.items(), key=lambda x: x[1], reverse=False)#将Mi中的元素按其影响力的大小从小到大排序
    Milist = []
    for i in range(len(list)):
        Milist.append(list[i][0])#Milist中存储Mi中的元素从小到大排序
    # print(Milist)
    Mi_index_list=[i for i in range(N)]
    Mi_index=sample(Mi_index_list,N)
    # print(N,Mi_index)
    for j in range(N):
        # print("==================")
        target_index=Mi.index(Milist[Mi_index[j]])
        #如果Dif_set中的顶点与Mi中相同，则从全局中取
        Interset = set(Can_set) & set(Mi)
        if len(Interset)==Can_set_num:
            v=getDifferentRandom(Mi,nodelist,k,eta,theta)
        else:
            index=random.randint(0,Can_set_num-1)
            while Can_set[index] in Mi:
                index = random.randint(0, Can_set_num-1)
                # print("+++++++++++++++")
            v=Can_set[index]
            # print(v)
        Mi[target_index]=v
        # print(Mi)
    # print(Mi)
    return Mi

def Mutation(X,nodelist,node_inf,F,pop,k,eta,theta):  #根据差分结果进行差分变异
    M=[]    #差分变异产生的中间体变量
    for i in range(pop):
        if isSame(X, pop) == True:
            index1=random.randint(0,pop-1)
            Xr1=LID_Search(nodelist,k,eta,theta)#X[index1]
            Xr2=LID_Search(nodelist,k,eta,theta)
            InterSet = set(Xr1) & set(Xr2)
            Dif_set = set(Xr1) - InterSet
            Dif_set = list(Dif_set)
        else:
            InterSet_num=k
            while k-InterSet_num==0:
                index1,index2,index3 = getThreeDifferentValue(pop)
                InterSet = set(X[index2]) & set(X[index3])
                InterSet_num = len(InterSet)
            Dif_set=set(X[index2])-InterSet
            Dif_set=list(Dif_set)
        Mi = singleMutation(X[index1],Dif_set, nodelist,node_inf, F, k,eta,theta)
        M.append(Mi)
    return M

def Crossover(M,X,nodelist,cr,pop,k):
    C=[]
    for i in range(pop):
        Ci=[]
        for j in range(k):
            if random.random()<cr:
                if M[i][j] not in Ci:
                    Ci.append(M[i][j])
                else:
                    if X[i][j] in Ci:
                      v = getDifferentRandom(Ci, nodelist, k,eta,theta)
                      Ci.append(v)
                    else:
                        Ci.append(X[i][j])
            else:
                if X[i][j] not in Ci:
                    Ci.append(X[i][j])
                else:
                    if M[i][j] in Ci:
                      v = getDifferentRandom(Ci, nodelist, k,eta,theta)
                      Ci.append(v)
                    else:
                        Ci.append(M[i][j])
        C.append(copy.copy(Ci))

    return C

def EDV(G,S,node_inf,k):  #二跳EDV
    inf=k
    active_dict={}
    Ne=[]
    for i in range(0, k):
        neighbors=G.neighbors(S[i])  #获取S[i]的邻居顶点
        Ne.extend(neighbors)
    Ne=set(Ne)-set(S)
    #一跳邻居顶点被激活的收益
    for u in Ne:
        other=1
        Peu=G.predecessors(u)
        Can=set(Peu)&set(S)
        for v in Can:
            other*=1-G[v][u]['weight']
        inf+=(1-other)*node_inf[u]#
        active_dict[u]=1-other
    twohop_Ne=[]
    #计算二跳邻居顶点
    for u in Ne:
        neighbors=G.neighbors(u)
        twohop_Ne.extend(neighbors)
    twohop_Ne=set(twohop_Ne)-set(S)-Ne
    #二跳邻居顶点被激活的收益
    for u in twohop_Ne:
        other = 1
        Peu = G.predecessors(u)
        Can = set(Peu) & Ne
        for v in Can:
            other *= 1 - G[v][u]['weight']*active_dict[v]
        inf += (1 - other)*node_inf[u]#
    return inf

#选择
def Selection(X,C,node_inf,pop):
    maxEDV=-100000
    maxEDV_Xi=[]
    for i in range(pop):
        #二跳EDV
        influence_xi=EDV(G,X[i],node_inf,k)
        influence_ci=EDV(G,C[i],node_inf,k)

        if influence_ci>influence_xi:
            X[i]=copy.copy(C[i])
            if influence_ci>maxEDV:
                maxEDV=influence_ci
                maxEDV_Xi=X[i]
        else:
            if influence_xi>maxEDV:
                maxEDV=influence_xi
                maxEDV_Xi=X[i]
    return X,maxEDV_Xi,maxEDV


