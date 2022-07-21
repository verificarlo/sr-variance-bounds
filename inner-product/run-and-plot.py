#!/usr/bin/env python3

"""
Accompagnying script to replicate the experiments in Figure 8 of the paper:
"Stochastic Rounding Variance and Probabilistic Bound: a New Approach"

Before running this script, please compile product.c with the following command
line:

verificarlo-c -O2 --function=dot_product_sr ./product.c -o product
"""


import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import axis, cm
import numpy as np
import matplotlib
import subprocess

# SR unit-roundoff
u = 2**(-23)

# lambda
lam = 0.1

# SR samples
sr_samples = 30

# n interval
n_values = [i*10**7  for i in [0.0078125, 0.015625, 0.031125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7]]

def verificarlo_run(n):
    """ simulate with verificarlo the inner-product of two vectors
    of n dimension with SR single precision
    """

    cmd = 'VFC_BACKENDS_LOGFILE="verificarlo.log" '
    cmd += 'VFC_BACKENDS="libinterflop_mca_int.so --precision-binary32=24" '
    cmd += './product {} {}'.format(n, sr_samples)
    samples = [float(s) for s in subprocess.getoutput(cmd).split()]
    # The first value is the reference computation in double
    return samples[0], np.array(samples[1:])

def ieee_run(n):
    """ compute the IEEE RN-binary32 deterministic result
    """

    cmd = 'VFC_BACKENDS_LOGFILE="ieee.log" '
    cmd += 'VFC_BACKENDS="libinterflop_ieee.so" '
    cmd += './product {} {}'.format(n, 1)
    samples = [float(s) for s in subprocess.getoutput(cmd).split()]
    return np.array(samples[1])


def error(x, ref):
    """ returns relative forward error """
    return abs((x-ref)/ref)

# Define plot title and labels
title = "-\lambda$ = {} ".format(1-lam)
plt.figure(title, figsize=(10, 8))
plt.suptitle(title)
plt.xlabel("$n$")
plt.xscale('log')
plt.yscale('log')
plt.ylabel("Error")

# RN-Binary32
ieee_error = []

# SR-Binary32
sr = [[] for _ in range(sr_samples)]
sr_average = []

# Bounds
azuma = []
cheby = []
dete_bound = []

# Compute all values and deterministic bounds across increasing n
for n in n_values:
    print(n)
    ref, samples = verificarlo_run(n)
    ieee_value = ieee_run(n)
    sr_average.append(error(np.mean(samples), ref))
    ieee_error.append(error(ieee_value, ref))
    for r in range(sr_samples):
        sr[r].append([error(samples[r],ref)])

    azuma.append(math.sqrt(u*((1+u)**(2*n)-1)*(math.log(2.0/(lam)))))
    cheby.append(math.sqrt(((1+(u)**2)**(n)-1)*(1.0/(lam))))
    dete_bound.append((1+u)**(n)-1)

# Plot the deterministic and probabilistic upper bounds on forward error
plt.plot(n_values, cheby, color='c', label = 'BC bound')
plt.plot(n_values, azuma, '--', color='g', label = 'AH bound')
plt.plot(n_values, dete_bound, linestyle=':', color='b', label = 'Deterministic bound')

# Plot RN and SR samples
for r in range(sr_samples):
    plt.plot(n_values, sr[r], ' v', color='r', label = 'SR-nearness' if r == 0 else '')

plt.plot(n_values, sr_average, ' o', color='k', label = 'SR-average')

plt.plot(n_values, ieee_error, ' *', color='y', label = "RN-binary32")


plt.legend()
plt.savefig("inner-product-plot.pdf", format='pdf')
plt.show()
