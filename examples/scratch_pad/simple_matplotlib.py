import matplotlib.pyplot as plt
import random

fig = plt.figure(figsize=(6,6))
ax = fig.add_axes([0.1,0.1,0.8,0.8])
x = [x for x in range(0,50)]
y = [random.randint(10,30) for y in range(0,50)]
ax.bar(x,y)

plt.show()
