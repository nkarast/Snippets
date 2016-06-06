"""
	This creates an "animated" movie of a scatter plot being filled
	element by element.

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


x = np.linspace(1,1000,50)
y = np.linspace(1000,2000, 50)

fig = plt.figure(figsize = (5,5))
axes = fig.add_subplot(111)
axes.set_xlim(min(x), max(x))
axes.set_ylim(min(y), max(y))
time_template = 'Turn = %i'
time_text = axes.text(0.05, 0.9, '', transform=axes.transAxes)

global t



def animate(coords):
	time_text.set_text(time_template % coords[2])
	return plt.scatter([coords[0]],[coords[1]], color='b'), time_text

def frames():
    for xt, yt, turn in zip(x, y, np.linspace(1,len(x))):
        yield xt, yt, turn

anim = animation.FuncAnimation(fig, animate,
                               frames=frames, interval=100, blit=False) #set to true, crashes on mac
anim.save("animate_map.mp4")
plt.show()


# ####-----

# import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib import animation
# import seaborn as sns

# nx = 50
# ny = 50

# fig = plt.figure()
# data = np.random.rand(nx, ny)
# sns.heatmap(data, vmax=.8, square=True)

# def init():
#       sns.heatmap(np.zeros((nx, ny)), vmax=.8, square=True)

# def animate(i):
#     data = np.random.rand(nx, ny)
#     sns.heatmap(data, vmax=.8, square=True)

# anim = animation.FuncAnimation(fig, animate, init_func=init, frames=20, repeat = False)
# anim.save("test.mp4")
# #plt.show()