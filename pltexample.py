from re import T
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

# pylab.plot(x_values,y_values,'ro')
# pylab.show()


import pandas as pandas

table=list("ABCDefg")
percent=[25,30,19,5,10,11,10]
explode=[0,0.01,0,0,0,0,0]
# plt.axes(aspect=1)
# plt.pie(percent,labels=table,autopct="%.2f%%",explode=explode,shadow=True)
# plt.show()

class American():
    def __init__(self):
        self.nationality="american"
    
    @staticmethod
    def print_nationality():
        print("american")

class NewYorker(American):
    pass

am1=American()
#NewYorker.print_nationality()

class Shape():
    def __init__(self,length):
         self.length=0
    def area(self):
        return 0

class square(Shape):
    def __init__(self,length):
        super(Shape, self).__init__()
        self.length=length
    def area(self):
        return self.length**2

a=square(4)
print(a.area())




























































