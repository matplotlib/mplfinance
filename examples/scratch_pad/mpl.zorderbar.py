import matplotlib.pyplot as plt

fig = plt.figure()

fig.patch.set_alpha(0.0)

ax0 = fig.add_axes( [0.1,0.1,0.8,0.8] )
ax1 = fig.add_axes( [0.1,0.1,0.8,0.8] )

print('ax0 zorder=',ax0.get_zorder())
print('ax1 zorder=',ax1.get_zorder())

ax0.set_zorder(0.1)

X  = [0,1,2,3,4]

Y0 = [2,4,3,5,3.5]
Y1 = [4600,4400,4800,4800,5000]


ax0.plot(X, Y0, linewidth=5, color='lime')
ax1.plot(X, Y1, linewidth=5, color='magenta')

# ax1.set_zorder(1)
# ax0.set_zorder(2)
# ax0.patch.set_visible(False)

plt.show()
