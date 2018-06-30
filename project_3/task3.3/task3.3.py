import csv
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# Fixing random state for reproducibility
np.random.seed(19680801)
NEUR_NUM = 10
TMAX = 1000


class SOM:
    def __init__(self, all_points, neurons_num, tmax):
        self.all_points = all_points
        self.neurons_num = neurons_num
        self.tmax = tmax
        self.neurons = self.choose_init_set(len(all_points), neurons_num)
        self.edges = [[i, i+1] for i in range(neurons_num - 1)]
        self.edges.append([neurons_num - 1, 0])
        self.edges = np.array(self.edges, dtype=np.int)
        dist = self.init_graph()
        self.dist = self.floyd_warshall(dist)

    def debug_run(self):
        for t in range(1, TMAX):
            point = self.choose_random_point(len(self.all_points))
            winner = self.choose_winner(point)
            self.update_neurons(point, winner, t)

    def run(self):
        # set up initial 3D visualization
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        y = self.all_points
        # fit data into the picture
        ax.set_xlim3d([np.min(y[:, 0]), np.max(y[:, 0])])
        ax.set_xlabel('X')
        ax.set_ylim3d([np.min(y[:, 1]), np.max(y[:, 1])])
        ax.set_ylabel('Y')
        ax.set_zlim3d([np.min(y[:, 2]), np.max(y[:, 2])])
        ax.set_zlabel('Z')
        # draw initial points set
        ax.scatter(y[:, 0], y[:, 1], y[:, 2], s=20, alpha=0.15)
        # draw initial neurons positions
        y = self.neurons
        neurons_plt = ax.scatter(y[:, 0], y[:, 1], y[:, 2], s=20, c='r', alpha=1.0)
        y = np.append(y, [y[0]], axis=0)
        edges_plt = ax.plot(y[:, 0], y[:, 1], y[:, 2], 'C3', zorder=1, lw=1)[0]
        anim = animation.FuncAnimation(fig, self.update_graph, frames=TMAX, fargs=(neurons_plt, edges_plt),
                                       interval=50)
        plt.show()

    def update_graph(self, t, neurons_plt, edges_plt):
        point = self.choose_random_point(len(self.all_points))
        winner = self.choose_winner(point)
        self.update_neurons(point, winner, t)
        print("current frame is " + str(t))
        y = self.neurons
        neurons_plt._offsets3d = np.array([y[:, 0], y[:, 1], y[:, 2]])
        y = np.append(y, [y[0]], axis=0)
        edges_plt.set_xdata(y[:, 0])
        edges_plt.set_ydata(y[:, 1])
        edges_plt.set_3d_properties(y[:, 2])
        return neurons_plt

    def update_neurons(self, x, i, t):
        new_neurons = []
        for j in range(self.neurons_num):
            coef = self.eta(t) * math.exp((-1.0 * self.dist[i][j]) / (2.0 * self.sigma(t)))
            delta = coef * (self.all_points[x] - self.neurons[j])
            new_neuron = self.neurons[j] + delta
            new_neurons.append(new_neuron)
        self.neurons = np.array(new_neurons)

    def sigma(self, t):
        return math.exp((-1.0 * t) / self.tmax)

    def eta(self, t):
        return 1 - t * 1.0 / self.tmax

    def choose_init_set(self, num, k):
        return np.array([self.all_points[self.choose_random_point(num)] for _ in range(k)])

    def choose_winner(self, point):
        winner = -1
        min_dist = sys.float_info.max
        for i in range(self.neurons_num):
            dist = self.eucl_dist(self.neurons[i], self.all_points[point])
            if dist < min_dist:
                min_dist = dist
                winner = i
        return winner

    def init_graph(self):
        num = self.neurons_num
        dist = np.full((num, num), np.inf)
        for i in range(num - 1):
            dist[i][i + 1] = 1
            dist[i + 1][i] = 1
            dist[i][i] = 0
        dist[num - 1][0] = 1
        dist[0][num - 1] = 1
        dist[num - 1][num - 1] = 0
        return dist

    def floyd_warshall(self, dist):
        num = self.neurons_num
        for t in range(num):
            for u in range(num):
                for v in range(num):
                    newdist = dist[u][t] + dist[t][v]
                    if newdist < dist[u][v]:
                        dist[u][v] = newdist
        return dist

    @staticmethod
    def eucl_dist(p1, p2):
        return np.linalg.norm(p1 - p2)

    @staticmethod
    def choose_random_point(num):
        return np.random.randint(0, num)


if __name__ == "__main__":
    with open("q3dm1-path1.csv") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        data = [r for r in reader]
        x = np.array(data)
        points = x.astype(np.float)
        som = SOM(points, NEUR_NUM, TMAX)
        som.run()

