"""
A simple example of TWO animated plots
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2,sharey=ax1)

x = np.arange(0, 2*np.pi, 0.01)

line1, = ax1.plot(x, np.sin(x))
line2, = ax2.plot(x, 0.5*np.sin(2.5*(x)))

def animate1(i):
    line1.set_ydata(np.sin(x + i/10.0))  # update the data
    return line1,

def animate2(i):
    line2.set_ydata(0.5*np.sin(2.5*(x + i/5.0)))  # update the data
    return line2,

ani1 = animation.FuncAnimation(fig, animate1, np.arange(1, 200), interval=250)

ani2 = animation.FuncAnimation(fig, animate2, np.arange(1, 200), interval=75)

plt.show()
