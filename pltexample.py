import matplotlib.pyplot as plt 
import numpy as np

x=np.linspace(0,10,1000)
y=np.sin(x)
z=np.cos(x**2)
# fig=plt.figure(figsize=(8,4))
# ax=fig.add_subplot(211)
# plt.subplot(2,1,1)

# plt.plot(x,y,label="$sin(x)$",color="red",linewidth=2)
# plt.ylabel("y Volt")
# plt.subplot(2,1,2)
# plt.plot(x,z,label="$cos(x^2)$",color="blue",linewidth=1)
# plt.ylabel("z Volt")
# plt.xlabel("Time(s)")
# ax.annotate('sin(x)',xy=(2,1),xytext=(3,1.5),
#             arrowprops=dict(facecolor="black",shrink=0.05))
# ax.set_ylim(0.2,2)
#plt.show()

import pylab,math

x_values=[]
y_values=[]
num=0.0

while num<math.pi*4:
    y_values.append(math.sin(num))
    x_values.append(num)
    num+=0.1

pylab.plot(x_values,y_values,'ro')
pylab.show()





































