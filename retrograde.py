import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create new Figure and an Axes which fills it
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], xlim=(-1.2, 1.2), ylim=(-1.2, 1.2))
ax.axis('off')

# Create planet data
t = np.linspace(0, 2 * np.pi, 500)  # time array
x = np.cos(t) - 0.2 * np.cos(9 * t)  # simplified x position (planet's longitude)
y = np.sin(t) - 0.2 * np.sin(9 * t)  # simplified y position (planet's latitude)

# Create planet object, which we will update during animation
planet, = ax.plot([], [], 'o', color='blue')


def init():
    # Initialize animation
    planet.set_data([], [])
    return planet,


def update(i):
    # Update animation for each frame
    if i < 200 or 300 < i:  # simulate normal motion
        planet.set_data([x[i]], [y[i]])
    else:  # simulate retrograde motion
        planet.set_data([x[i]], [y[i]])
    return planet,


# Create animation
ani = FuncAnimation(fig, update, frames=range(len(t)), init_func=init, blit=True)

ani.save('planet_motion.mp4', writer='ffmpeg')

plt.show()
