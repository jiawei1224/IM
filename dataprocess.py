import networkx as nt
import random
import networkx
import random
import time
import sys
import numpy as np
def readdata():
    # u=dict()
    # u[1] = [1, 2, 5]
    # u[2] = [1, 3, 6]
    # u[3] = [1,4, 5, 6]
    # u[4] = [2, 3, 5, 6, 7]
    topics = ['a','b','c','d']
    s=dict()
    stp=['a']
    s['a','b']=s['b','a']=0.1
    s['a','c']=s['c','a']=0.3
    s['a','d'] =s['d','a'] =0.6
    s['b','c']=s['c','b']=0.1
    s['b','d']=s['d','b']=0.7
    s['c','d']=s['d', 'c']=0.2
    s['a','a']=s['b','b']=s['c','c']=s['d','d']=1

    with open("D:/dataset/IM/oregon1_0105123.txt", "r") as ppi:
        # Empty network graph
        U = dict()
        G = nt.DiGraph()
        for l in sorted(G.nodes):
            U[l] = random.sample(topics, 1)  # 随机生成时间序列 第一个为随机选择，第二个为随机个数
        # print("用户时间序列信息", U)
        st=dict()
        for n in U.keys():
            st[n]=s[U[n][0],stp[0]]
        to=0
        for k,v in st.items():
           to=to+v
        ave=to/len(st.keys())
        print("平均主题",ave)
        # print("给定的主题为",stp)
        # print("用户主题相关度为",st)
        # for k, v in st.items():
        #     print(k, v)
        #     outputfile = open("D:\\dataset\\IM\\Markov\\tp.txt", "a")
        #     sys.stdout = outputfile
        return st


def stactics1():   #计算一阶概率
    u=readdata()
    la = dict()   #用来存储倒数第一个值
    t2 =[]   #所有值
    for k, v in u.items():
        t2 = t2 + v
        la[k] = v[len(v) - 1]
    # ts=dict()    #统计间隔
    # t = []
    # for k,i in u.items():
    #     for x, y in zip(i[0::], i[1::]):
    #         t.append(y-x)
    #     ts[k]=t
    # for k, i in ts.items():
    #     t3 = t3 + i
    # for i in set(t3):
    #     t4[i] = t3.count(i) / len(t3)
    # print("一阶",t4)
    return la

def stactics2():    #计算二阶概率
    u=readdata()
    la2 = dict()   #用来存储倒数第二个值
    t2 =[]
    t5 = []  # 二阶差值
    t6 = dict()  # 计算二阶相邻间隔的概率
    for k,i in u.items():
        t2=t2+i
        la2[k]=i[len(i)-2]
    ts2 = dict()  # 统计间隔2
    t = []
    for k, i in u.items():
        if len(i) > 2:
            for x, y in zip(i[0::], i[2::]):
                t.append(y - x)
        # if len(i) > 3:
        #     for x, y in zip(i[1::], i[3::]):
        #         t.append(y - x)
        # if len(i) > 4:
        #     for x, y in zip(i[2::], i[4::]):
        #         t.append(y - x)
        else:
            sum = 0
            for item in i:
                sum += item
            la2[k] = int(sum / len(i))
        ts2[k] = t

    for k, i in ts2.items():
        t5 = t5 + i
    for i in set(t5):
        t6[i] = t5.count(i) / len(t5)
    # print("二阶",t6)
    return t6,la2


def computet():
    u=readdata()
    p1=dict()
    ip=11   #输入时间
    la=stactics1()
    t2,la2=stactics2()
    t1,pc=stactics()
    # t3,la3 =stactics3()
    for k,i in u.items():
            if ip-la[k] in t1.keys():
                p1[k]=t1[ip-la[k]]
                # print(k,t4[ip-la[k]])
            else:
                if la[k] - la2[k] in t1.keys():
                    p1[k] = t1[la[k] - la2[k]]
                p1[k] = 0
    # 判断新的与倒数第二个时间的差值来计算其概率
    p2=dict()
    for k,i in u.items():
            if ip-la2[k] in t2.keys():
                p2[k]=t2[ip-la2[k]]
                # print(k,t6[ip-la2[k]])
            else:
                p2[k]=0

    p3=dict()
    # print(t3.keys())
    for k,i in u.items():
        # print((ip - la[k], ip - la2[k]))
        if (la[k]-la2[k],ip-la[k]) in pc.keys():
            p3[k]=pc[(la[k]-la2[k],ip-la[k])]
        else:
            p3[k] = 0
    p=dict()
    for k, i in u.items():
        p[k]=(p1[k]+p2[k]+p3[k])/3 #三个权重求平均
    # print("时间活跃度",p)
    print("输入时间",ip,)
    return p

