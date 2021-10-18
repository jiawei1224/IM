import os
import pickle
import sys
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
# from IC import runIC
from scipy.special import comb, perm
from priorityQueue import PriorityQueue as PQ
# import Markov1
from DiGraph import ReadFileConstructGraph
import relatedtopicdegree
import random
import time
from IC1 import getICInfluence
import math
import networkx as nt
sys.setrecursionlimit(50000)

def Sampling(G,k,limit,l):
    nodedict={}   #记录顶点出现的次数
    R=[]
    LB=1
    tp = relatedtopicdegree.readdata()   #主题
    limit1=limit*math.sqrt(2)
    n=len(list(G.nodes))
    com=math.log(comb(n,k))
    # stp=dict()   #每个节点的在R中出现的次数乘以其主题
    stp1 = dict()  # 每个RR集的主题之和
    stp2 = dict()  # 每个RR集的主题之和

    for i in range(1,int(math.log(n,2))):
        x = n / (2 ** i)
        par = (2 + 2 * limit1 / 3) * (com + l * math.log(n, math.e) + math.log(math.log(n, 2), math.e)) * n / (
                    limit1 * limit1)
        # print(comb(n,k))
        numi=par/x
        # print(numi)
        while len(R)<=numi:
            index=random.randint(0,n-1)
            node=list(G.nodes)[index]
            # node=random_pick()
            Rj=getPointRR(G,nodedict,len(R),node)
            R.append(Rj)
            # if tp[Rj[len(Rj)-1]]>0.4:    #添加过滤条件initial：主题和时间活跃度
            #    R.append(Rj)


        # print("=================")
        Si,Sicov=NodeSelection(R,nodedict,k,stp4)
        # print(n*Sicov,(1+limit1)*x)
        if n*Sicov>=(1+limit1)*x:
            LB=n*Sicov/(1+limit1)
            break
    print(LB)
    a=(l*math.log(n,math.e)+math.log(2,math.e))**0.5
    # print(a)
    b=((1-1/math.e)*com+l*math.log(n,math.e)+math.log(2,math.e))**0.5
    # print(b)
    par1=2*n*(((1-1/math.e)*a+b)**2)*limit**(-2)
    # print(a,b,par1)
    num=par1/LB
    print(num)

    while len(R)<=num:
        index = random.randint(0,n-1)
        node = list(G.nodes)[index]
        # node = random_pick()
        Rj = getPointRR(G,nodedict,len(R),node)
        R.append(Rj)
    # for i in range (1,len(R)):
    #     stp1[pickle.dumps(R[i])]=0
    #     l1=R[i]
    #     for x1 in l1:
    #         stp1[pickle.dumps(l1)]=stp1[pickle.dumps(l1)]+tp[x1]
    # for i1 in range(1,len(R)):
    #     l2 = R[i1]
    #     for x2 in l2:
    #         stp2.setdefault(x2, []).append(stp1[pickle.dumps(l2)])    #每个节点的主题为其路径上的主题之和
    # for k3,v3 in stp2.items():
    #     stp4[k3]=0
    #     for l4 in v3:
    #         stp4[k3]=stp4[k3]+l4    #覆盖的RR集的主题之和
    # print(stp4)
    # num1=sum(R, [])
    # for l1 in num1:
    #     stp[l1]=num1.count(l1)*tp[l1]
    # print("stp",stp)

    return R,nodedict,stp4


def NodeSelection(R,nodedict,k,stp4):
    S=[]
    Q=PQ()
    Sinfluence=0
    havedeleteRegion=[]  #存储已经被排除的抽样
    stp1 = dict()  # 每个RR集的主题之和
    stp2 = dict()  # 每个RR集的主题之和
    tp = relatedtopicdegree.readdata()  # 主题
    for i in range (1,len(R)):
        stp1[pickle.dumps(R[i])]=0
        l1=R[i]
        for x1 in l1:
            if x1 in tp.keys():
               stp1[pickle.dumps(l1)]=stp1[pickle.dumps(l1)]+tp[x1]
            else:
               stp1[pickle.dumps(l1)] = stp1[pickle.dumps(l1)] + 0
    for i1 in range(1,len(R)):
        l2 = R[i1]
        for x2 in l2:
            stp2.setdefault(x2, []).append(stp1[pickle.dumps(l2)])    #每个节点的主题为其路径上的主题之和
    for k3,v3 in stp2.items():
        stp4[k3]=0
        for l4 in v3:
            stp4[k3]=stp4[k3]+l4    #覆盖的RR集的主题之和
    R2=sum(R, [])
    t5=0
    for l5 in R2: #R中主题总和
        if l5 in tp.keys():
           t5=t5+tp[l5]
        else:
            t5 = t5 + 0
    # print('111',stp4)
    for node, nodeRRset in nodedict.items():
        if node in stp4.keys():
            r1=stp4[node]
        else:
            r1=0
        Q.add_task(node,-r1*len(nodeRRset))    #覆盖的主题乘以长度最大的
    for i in range(k):
        node,cov=Q.pop_item()
        if node in S:
            continue
        # print(node)
        Sinfluence+=-cov/len(nodeRRset)
        S.append(node)
        C=[]  #存储node所在反向可达集中的其他顶点
        # print(nodedict[node])
        for RRsetId in nodedict[node]:
            # C.extend(R[RRsetId])
            if RRsetId in havedeleteRegion:
                continue
            havedeleteRegion.append(RRsetId)
            # print(RRsetId,R[RRsetId])
            for v in R[RRsetId]:
                if v in S:
                    continue
                [priority, count, task] = Q.entry_finder[v]
                # print(v,priority+1)
                Q.add_task(v,priority+1)
    # sum1=0
    # for x in S:
    #     if x in tp.keys():
    #       sum1=sum1+stp4[x]
    #     else:
    #       sum1=sum1+0
    print("Sinfluence:{}".format(Sinfluence))
    # print(Sinfluence)
    return S,Sinfluence

