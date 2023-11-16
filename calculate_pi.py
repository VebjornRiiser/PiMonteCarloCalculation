from math import pi
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import random

# Iterator reads from random_numbers.txt file gotten from random.org
class RandomNumberIterator:
    def __init__(self):
        self.file = open('random_numbers.txt', 'r')

    def __iter__(self):
        return self

    def __next__(self):
        line = self.file.readline()
        if line:
            return [int(n) for n in line.strip().split('\t')]
        else:
            self.file.close()  # Close the file when done
            raise StopIteration


# Create an instance of the iterator
random_numbers = RandomNumberIterator()



# Prepare the plot
radius = 500
points_per_animation_step = 100
inside_count = 1
outside_count = 1
fig, ax = plt.subplots()
x_inside, y_inside = [], []
x_outside, y_outside = [0], [0]
sc_inside = ax.scatter(x_inside, y_inside, color='green')  # Points inside the circle
sc_outside = ax.scatter(x_outside, y_outside, color='red')  # Points outside the circle
plt.xlim(0, radius*2)
plt.ylim(0, radius*2)



# Draw a circle
circle = Circle((radius, radius), radius, fill=False, color='blue', linewidth=2)
ax.add_patch(circle)

text = ax.text(5, radius*2 - 50, '', fontsize=12,
               bbox=dict(facecolor='white', alpha=1, edgecolor='black'))



def update(frame):
    global inside_count, outside_count, points_per_animation_step
    for i in range(points_per_animation_step):
        point = next(random_numbers)
        if inside_circle(*point, radius):
            x_inside.append(point[0])
            y_inside.append(point[1])
            inside_count += 1
        else:
            x_outside.append(point[0])
            y_outside.append(point[1])
            outside_count += 1

    sc_inside.set_offsets(list(zip(x_inside, y_inside)))
    sc_outside.set_offsets(list(zip(x_outside, y_outside)))

    ratio = inside_count / (inside_count + outside_count)
    pi_estimate = 4*ratio
    text.set_text(f"n = {outside_count+inside_count}, Pi estimate = {pi_estimate}, Deviation: {abs(pi-pi_estimate)}")
    return sc_inside, sc_outside 

def inside_circle(x_p, y_p, r):
    return (x_p-r)**2+(y_p-r)**2 < r*r
    # (y+a)^2+(x+b)^2=r^2


def init_animation():  # initialization function
    sc_outside.set_offsets([[x_outside[0], y_outside[0]]])
    return sc_outside

# Create animation
ani = animation.FuncAnimation(fig, update, init_func=init_animation, interval=1)
plt.show()
