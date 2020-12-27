import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor

print('1')
t = np.arange(0.0, 2.0, 0.01)
s1 = np.sin(2*np.pi*t)
s2 = np.sin(4*np.pi*t)

print('2')
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.plot(t, s1)
ax2.plot(t, s2)

print('3')
multi = MultiCursor(fig.canvas, (ax1, ax2), color='lime', lw=1, horizOn=True, vertOn=True)
print('4')
plt.show()
