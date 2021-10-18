from DiGraph import ReadFileConstructGraph
from IC1 import getICInfluence
from priorityQueue import PriorityQueue as PQ
#from NetWork.LT import getLTInfluence
import random
import copy
import time
#from scipy.special import comb
import math
import relatedtopicdegree

def Sampling(G,k,limit,l):
    nodedict={}   #记录顶点出现的次数
    R=[]
    LB=1
    limit1=limit*math.sqrt(2)
    n=len(list(G.nodes))
    com=getPar(n,k)
    par=(2+2*limit1/3)*(com+l*math.log(n,math.e)+math.log(math.log(n,2),math.e))*n/(limit1*limit1)
    for i in range(1,int(math.log(n,2))):
        x=n/(2**i)
        # print(comb(n,k))
        numi=par/x
        # print(numi)
        while len(R)<=numi:
            index=random.randint(0,n-1)
            node=list(G.nodes)[index]
            Rj=getPointRR(G,nodedict,len(R),node)
            R.append(Rj)
        # print("=================")
        Si,Sicov=NodeSelection(R,nodedict,k)
        # print(n*Sicov,(1+limit1)*x)
        if n*Sicov>=(1+limit1)*x:
            LB=n*Sicov/(1+limit1)
            break
    # print(LB)
    a=(l*math.log(n,math.e)+math.log(2,math.e))**0.5
    # print(a)
    b=((1-1/math.e)*com+l*math.log(n,math.e)+math.log(2,math.e))**0.5
    # print(b)
    par1=2*n*(((1-1/math.e)*a+b)**2)*limit**(-2)
    # print(a,b,par1)
    num=par1/LB
    # print(num)
    while len(R)<=num:
        index = random.randint(0,n - 1)
        node = list(G.nodes)[index]
        Rj = getPointRR(G,nodedict,len(R),node)
        R.append(Rj)
    return R,nodedict


def NodeSelection(R,nodedict,k):
    S=[]
    Q=PQ()
    Sinfluence=0
    havedeleteRegion=[]  #存储已经被排除的抽样
    for node, nodeRRset in nodedict.items():
        Q.add_task(node,-len(nodeRRset))
    for i in range(k):
        node,cov=Q.pop_item()
        if node in S:
            continue
        # print(node)
        Sinfluence+=-cov
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
    print("Sinfluence:{}".format(Sinfluence/len(R)))
    # print(Sinfluence)
    return S,Sinfluence/len(R)

