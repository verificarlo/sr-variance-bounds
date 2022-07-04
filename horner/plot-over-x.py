#!/usr/bin/python3

import sys
import re
import numpy as np

import matplotlib
from fractions import Fraction
from numpy.lib.type_check import real
# Use Agg backend for headless runs
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import math

# error function
def error(x, ref):
    """ returns relative forward error """
    return abs((x-ref)/ref) 

# SR unit-roundoff
u = 2**(-23)

# lambda
lam = 0.1

# Define plot title and labels
title = "$1-\lambda$ = {} ".format(1-lam)
plt.figure(title, figsize=(7, 5))
plt.suptitle(title)
plt.xlabel("$x$")
plt.yscale('log')
plt.ylim((10**(-8), 10**2)) 
plt.ylabel("$Error$")

# coef
a = []

# 2*(polynomial degree)
N = int(sys.argv[1])

# read all coef from file
f = open('result'+ str(N) +'.txt', 'r')
for line in f:
    a.append(float(line))    

# polynomial degree
n= N/2 

# gamma
gamma2 = (1+u)**(2*n) -1 
gamma4 = (1+u)**(4*n) -1 
gamma = (1+u**2)**(2*n) -1 

# denominator 
deno = int(sys.argv[2])

# bounds
det_bound = []
azuma = []
cheby = []

# SR_average    
sr_average = []

# RN-error
ieee_k = []

# x values
array_x = []

k = 8
while k < (deno + 1):
    # exact value p(x)
    f = open('resultt'+ sys.argv[1] + str(k)+ '.txt', 'r')
    for line in f:
        Txx = float(Fraction(line))

    # x value 
    x = Fraction(k,deno) 

    # absp = p(valeur absolue)
    absp = abs(a[0]) 
    for i in range(1,len(a)):
         absp  =  absp  + abs(a[i]*(x**(2*i)))
         
    # RN-binary32 forward errors     
    f = open('ieee_'+ str(k) +'.tsv', 'r')
    ieee_k.append( error( float(f.read()), Txx) )
 
    # read all results from file
    dtype3 = np.dtype([('res', np.float32)]) 
    D = np.loadtxt('global_'+ str(k) +'.tsv', skiprows=0, dtype = dtype3)
    
    # 30 times the x value
    array_k = []

    # SR errors
    sr = [] 

    # forward error/cond(P)
    for i in range(30):
        array_k.append(x)
        sr.append( error(D['res'][i], Txx))

    # forward error of the average of the 30 SR samples    
    sr_average.append(error( np.mean(np.array(D['res'])), Txx))

    
    det_bound.append( gamma2*absp/ abs(Txx) )
    azuma.append( absp*math.sqrt(u*gamma4*math.log2(2.0/lam))/abs(Txx))
    cheby.append( absp*math.sqrt(gamma*(1.0/lam))/abs(Txx))
    
    array_x.append(x)

    # plot SR points
    if k== deno:
        plt.plot(array_k, sr, 'v', color='r', label = 'SR-nearness')

    plt.plot(array_k, sr, 'v', color='r')
    
    
    k=k+2

# Plot the deterministic and probabilistic upper bounds on forward error
plt.plot(array_x, det_bound, linestyle=':', color='b', label = "Deterministic bound")
plt.plot(array_x, azuma, '--', color='g', label = "AH bound")
plt.plot(array_x, cheby, color='c', label = "BC bound")

#Plot RN samples
plt.plot(array_x, ieee_k, ' *', color='y', label = "RN-binary32")

# Plot the forward error of the average of the 30 SR samples    
plt.plot(array_x, sr_average, ' o', color='k', label = "SR-average")


plt.show()
plt.legend()

plotname = "horner-plot-" + sys.argv[1] +".pdf"
plt.savefig(plotname, format='pdf')    
