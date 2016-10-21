import numpy as np
import numba as nb
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


class Particles:
  def __init__(self, mean=[0,0,0], cov=[[1,0,0], [0,1,0], [0,0,0.1]], N=1000):
    self.mean = mean
    self.cov  = cov
    self.N    = N
    self.generate_Particles()

    self.reset_x
    self.reset_y
    self.reset_z

  def generate_Particles(self):
    self.x , self.y, self.z = np.random.multivariate_normal(self.mean, self.cov, self.N).T
    self.reset_x, self.reset_y, self.reset_z = self.x , self.y, self.z

  def plot_distribution(self):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(self.x,self.y,self.z, c = 'red', alpha=0.3)
    ax.set_xlabel('X [a.u.]')
    ax.set_ylabel('Y [a.u.]')
    ax.set_zlabel('Z [a.u.]')
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_zlim(-5,5)
    plt.grid(True)
    plt.show()

  def move_distribution(self,t):

    self.x += np.sqrt(3.75)*np.cos(10*t)
    self.y += np.sqrt(3.75)*np.cos(20*t)
    self.z += 2*t #100+np.sqrt(3.75)*np.cos(0.5*t)

  def reset_distribution(self):
    self.x = self.reset_x
    self.y = self.reset_y
    self.z = self.reset_z


## Mean values and Covariance matrix for gaussian
# mean = [0,0,0]
# cov = [[1,0,0], [0,1,0], [0,0,0.1]]

# x, y, z = np.random.multivariate_normal(mean, cov, 1000).T
#print x, "\n\n", y, "\n\n", z

#plt.ion()

distr = Particles(N=10)

fig = plt.figure(figsize = (7,7))
axes = fig.add_subplot(111, projection='3d')
time_template = 't = %.2f'
time_text = axes.text(0.05, 0.9, 0.9,'', transform=axes.transAxes)

def animate(coords):
  time_text.set_text(time_template % coords[3])

  axes.set_xlabel('X [a.u.]')
  axes.set_ylabel('Y [a.u.]')
  axes.set_zlabel('Z [a.u.]')
  axes.set_xlim(-2,10)
  axes.set_ylim(-2,10)
  axes.set_zlim(-2,5000)
  plt.grid(True)
  return axes.scatter([coords[0]],[coords[1]], [coords[2]], c='red', alpha=0.2),time_text
  

def frames():
    for t in np.arange(0,50,1):
        distr.move_distribution(t)
        yield distr.x, distr.y, distr.z, t




anim = animation.FuncAnimation(fig, animate,
                               frames=frames, interval=100, blit=False, repeat=False)
#plt.show()
#plt.clf()

## ----------------------------------
distr.reset_distribution()

fig2 = plt.figure(figsize = (7,7))
axes2 = fig2.add_subplot(111)
def animate2(coords):
  time_text.set_text(time_template % coords[2])
  axes2.set_xlim(-2,10)
  axes2.set_ylim(-2,10)
  axes2.set_xlabel("X")
  axes2.set_ylabel("Y")
  plt.grid(True)
  return plt.scatter([coords[0]],[coords[1]], c='g', marker='^', alpha=0.5),time_text



def frames2():
    for t in np.arange(0,100,1):
        distr.move_distribution(t)
        yield distr.x, distr.y, t
ani2 = animation.FuncAnimation(fig2, animate2,
                               frames=frames2, interval=100, blit=False, repeat=False)


plt.show()

# print distr.x.shape
# distr.plot_distribution()

# distr.move_distribution(20)
# distr.plot_distribution()
# for t in np.arange(0,5,1):
#   distr.move_distribution(t)
#   distr.plot_distribution()
