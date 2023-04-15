# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 19:37:48 2023

@author: wyx
"""

from KKTmatrix import c,G, M,  E, h,G1, M1,  E1, h1
from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt
# 以KKT方法求解
# 建立主问题
tral = []
LB = -GRB.INFINITY
UB = GRB.INFINITY
lb = []
ub = []
MP = Model("MP")
x = MP.addMVar((48,),vtype=GRB.BINARY,name='x_MP')
y_mp = MP.addMVar((240,), lb=-GRB.INFINITY, name='y_mp')
u_mp = MP.addMVar((48,),vtype=GRB.BINARY,name='u_mp')
alpha = MP.addMVar((1,),obj=1,vtype=GRB.CONTINUOUS,name='alpha')
MP.addConstr(alpha>=c.T@y_mp)
MP.addConstr(G@y_mp >= h-M@u_mp-E@x, name="G1")
MP.addConstr(G1@y_mp == h1-M1@u_mp-E1@x, name="G2")
MP.optimize()
MP_obj = MP.ObjVal
LB = max(MP_obj, LB)

bigM = 10**4
k = 1
SP = Model('SP')
y = SP.addMVar((240,), lb=-GRB.INFINITY, name='y')
u = SP.addMVar((48,),vtype=GRB.BINARY,name='u')
pi1 = SP.addMVar((G.shape[0],), lb=-GRB.INFINITY,vtype=GRB.CONTINUOUS, name='pi1')
pi2 = SP.addMVar((G1.shape[0],),lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name='pi2')
v = SP.addMVar((G.shape[0],), vtype=GRB.BINARY, name='v')
w = SP.addMVar((G.shape[1],), vtype=GRB.BINARY, name='w')
l = SP.addMVar((G1.shape[0],), vtype=GRB.BINARY, name='l')

G11 = SP.addConstr(G@y >= h-M@u-E@x.x, name="G1")
G2 = SP.addConstr(G1@y == h1-M1@u-E1@x.x, name="G2")

SP.addConstr(G.T@pi1+G1.T@pi2<=c, name='pi')

SP.addConstr(pi1 <= bigM*v, name='v1')
G3 = SP.addConstr(G@y-h+E@x.x+M@u <= bigM*(1-v), name='v2')
SP.addConstr(pi2 <= bigM*l, name='l1')
G4 = SP.addConstr(G1@y-h1+E1@x.x+M1@u <= bigM*(1-l), name='l2')
SP.addConstr(y <= bigM*w, name='w1')

SP.addConstr(c-G.T@pi1-G1.T@pi2 <= bigM*(1-w), name='w2')

SP.addConstr(y>=0)
SP.addConstr(pi1>=0)
SP.setObjective(c@y, GRB.MAXIMIZE)
SP.optimize()
UB = min(SP.objVal, UB)
tral.append(abs(UB-LB))
lb.append(LB)
ub.append(UB)
# while abs(UB-LB) >= epsilon:
for _ in range(5):
    MP.reset()
    # add x^{k+1}
    y_new = MP.addMVar((240,), lb=-GRB.INFINITY,vtype=GRB.CONTINUOUS)
    # eta>=bTx^{k+1}
    MP.addConstr(alpha >= c.T@y_new)
    MP.addConstr(G@y_new>=h-E@x-M@u.x)
    MP.addConstr(G1@y_new==h1-E1@x-M1@u.x)
    # Ey+Gx^{k+1}>=h-Mu_{k+1}
    SP.reset()
    MP.optimize()
    MP_obj = MP.objval
    LB = max(LB, MP_obj)
    SP.remove(G11)
    SP.remove(G2)
    SP.remove(G3)
    SP.remove(G4)
    SP.update()
    G11 = SP.addConstr(G@y >= h-M@u-E@x.x, name="G1")
    G2 = SP.addConstr(G1@y == h1-M1@u-E1@x.x, name="G2")
    G3 = SP.addConstr(G@y-h+E@x.x+M@u <= bigM*(1-v), name='v2')
    G4 = SP.addConstr(G1@y-h1+E1@x.x+M1@u <= bigM*(1-l), name='l2')
    SP.update()
    SP.optimize()
    # obtain the optimal y^{k+1}
    SP_obj = SP.ObjVal
    UB = min(UB, SP_obj)
    k += 1
    tral.append(abs(UB-LB))
    lb.append(LB)
    ub.append(UB)
    if abs(UB-LB)<=10:
        break
    # go back to the MP
    print("经过{}次迭代".format(k))
    print("上界为：{}".format(UB))
    print("下界为：{}".format(LB))
    
def plot_figure():
    plt.figure(1)
    Pg = plt.bar(range(24),y.x[:24])
    plt.figure(2)
    Ps_ch = plt.bar(range(24),y.x[24:48])
    plt.figure(3)
    Ps_dis = plt.bar(range(24),y.x[48:72])
    plt.figure(4)
    Pdr = plt.bar(range(24),y.x[72:96])
    plt.figure(5)
    Pbuy = plt.plot(range(24),y.x[144:168])
    Psell = plt.plot(range(24),y.x[168:192])
    plt.figure(6)
    Ppv = plt.plot(range(24),y.x[192:216])
    Pl = plt.plot(range(24),y.x[216:240])
plot_figure()