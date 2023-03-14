"""
A simple example of TWO curves from one func animation
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure(figsize=(8*0.66,4*0.66))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2,sharey=ax1)

x = np.arange(0, 2*np.pi, 0.02)

line1, = ax1.plot(x, np.sin(x))
line2, = ax2.plot(x, 0.5*np.sin(2.5*(x)))

def animate(i):
    line2.set_ydata(0.5*np.sin(2.5*(x + i/5.0)))  # update the data
    if i%3 == 0:
        line1.set_ydata(np.sin(x + i/10.0))  # update the data
    return line1,line2

ani1 = animation.FuncAnimation(fig, animate, np.arange(1, 100), interval=250)

#  writergif = animation.PillowWriter(fps=5)
#  ani1.save('s2c.gif',writer=writergif)

plt.show()
