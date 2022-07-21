#!/usr/bin/python3

import sys
import re
import numpy as np
import os

import matplotlib
from numpy.lib.type_check import real
# Use Agg backend for headless runs
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import math
from fractions import Fraction

def coefs(n):
    T0 = {0:1}
    T1 = {1:1}
    for i in range(3,n+2):
        A = dict([(n+1, c*2) for n,c in T1.items()])
        B = dict([(n,-c) for n,c in T0.items()])
        T2 = {}
        for i in range(i):
            c = A.get(i, 0) + B.get(i, 0)
            if c != 0:
                T2[i] = c

        T0 = T1
        T1 = T2

    #print("Coeffs. Tchebychev T" + str(i))
    cfs = list(T1.items())
    cfs.sort()
    return cfs
    #print(cfs)

# polynomial degree
N = int(sys.argv[1])

# coef
cs = coefs(N)

f = open("result"+str(int(sys.argv[1]))+".txt", "w")  
for p,a in cs:
    f.write(str(a)+"\n")
f.close()

# x value
x=Fraction(int(sys.argv[2]), int(sys.argv[3]))

cs.sort(reverse=True)

# p(x)
def eval(x, coefs):
    x2 = x*x
    s = Fraction(0,1)
    for p,a in coefs:
        s = s*x2 + a
    return s

f = open("resultt"+str(int(sys.argv[1]))+str(int(sys.argv[2]))+".txt", "w")  
l = eval(x, cs)
f.write(str(l))
f.close()








