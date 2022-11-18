import numpy as np
import math
import matplotlib.pyplot as plt


x = np.linspace(0, 1, 30)
y1 = np.sqrt(2*np.log(2.0/(1-x)))
y2 = np.sqrt((1.0/(1-x)))

#plt.plot(x, y)
plt.xlabel("$1-\lambda$")
plt.ylabel("$f(\lambda)$")
plt.plot(x, y1, color='b', label = "$\sqrt{2ln(2/(1-\lambda))}$")
plt.plot(x, y2, ' +', color='r', label = "$\sqrt{1/(1-\lambda)}$")

delta = np.array([yy1-yy2 for yy1,yy2 in zip(y1,y2)])
idx = np.argwhere(np.diff(np.sign(delta))).flatten()[0]
plt.plot(x[idx], y1[idx], 'ro')
print("intersection = %g"%float(x[idx]))

plt.legend()
plt.yscale('log')
#plt.show()

plotname = "compare.pdf"
plt.savefig(plotname, format='pdf')
