import matplotlib.pyplot as plt
import timeit
import random

def pbar():
    fig = plt.figure(figsize=(5,2))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    x = [x for x in range(0,150)]
    y = [random.randint(10,30) for y in range(0,150)]
    ax.bar(x,y)
    
def pline():
    fig = plt.figure(figsize=(5,2))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    x = [x for x in range(0,150)]
    y = [random.randint(10,30) for y in range(0,150)]
    ax.plot(x,y)

timeline = timeit.timeit(pline,number=5)
timebar  = timeit.timeit(pbar,number=5)
print('timeline=',timeline)
print('timebar =',timebar)
print('\ntimebar/timeline=',timebar/timeline)

