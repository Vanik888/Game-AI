import csv
import numpy as np
import random
import sys
import math

NEUR_NUM = 10
TMAX = 100


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
        self.dist = self.floydwarshall(dist)

    def run(self):
        for t in range(TMAX):
            point = self.choose_random_point(len(self.all_points))
            winner = self.choose_winner(point)
            self.update_neurons(point, winner, t)

    def update_neurons(self, x, i, t):
        new_neurons = []
        for j in range(self.neurons_num):
            new_neuron = self.neurons[j] + \
                         self.eta(t) * math.exp((-1.0 * self.dist[i][j]) / 2.0 * self.sigma(t)) \
                         * (x - self.neurons[j])
            new_neurons.append(new_neuron)
        self.neurons = new_neurons

    def sigma(self, t):
        return math.exp((-1.0 * t)/ self.tmax)

    def eta(self, t):
        return 1 - t*1.0/self.tmax

    def choose_init_set(self, num, k):
        return [self.all_points[self.choose_random_point(num)] for _ in range(k)]

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

    def floydwarshall(self, dist):
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
        return random.randint(0, num)


if __name__ == "__main__":
    with open("q3dm1-path1.csv") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        data = [r for r in reader]
        x = np.array(data)
        y = x.astype(np.float)
        som = SOM(y, NEUR_NUM, TMAX)
        som.run()

