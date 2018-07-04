import logging
import sys
import csv
import numpy as np
from sklearn.cluster import KMeans
from math import sqrt

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(levelname)s | %(asctime)s | %(message)s')
logger = logging.getLogger('Logger from Task 2.2')


N_CLUSTERS = 10
ITERATIONS = 1000
USER_STATE_FILE = 'q3dm1-path1.csv'
NEURONS_STATE_FILE = 'neurons.csv'

def get_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        data = [i for i in reader]
        return np.array(data, dtype=np.float)


def get_activities(user_state_file):
    data = get_data(user_state_file)
    activities = np.full([len(data), 3], -1, dtype=np.float)
    for i in range(len(data)-1):
        activities[i] = data[i+1] - data[i]
    # connect the last and the first coordinates
    activities[len(data)-1] = data[0] - data[-1]
    return activities


def clusterise(data, clusters):
    mapping_array = np.full([len(data), 1], 0, dtype=np.int)

    for i, d in enumerate(data):
        for j, c in enumerate(clusters):
            dist = np.linalg.norm(d-c)
            if dist < np.linalg.norm(d-clusters[mapping_array[0]]):
                logger.debug('point %s (%s) = cluster %s (%s)'
                             % (d, i, c, j))
                mapping_array[i] = j
    return mapping_array

def policy(joint, s):
    return np.argmax(joint[s, :])

def euclidean(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)

def getCluster(x, neurons):
    dist = float('inf')
    ind = -1
    for i, neuron in enumerate(neurons):
        if euclidean(x, neuron) < dist:
            dist = euclidean(x, neuron)
            ind = i
    return i

if __name__ == '__main__':
    x = get_data(USER_STATE_FILE)
    neurons = get_data(NEURONS_STATE_FILE)
    activities = get_activities(USER_STATE_FILE)
    kmean = KMeans(n_clusters=N_CLUSTERS,
                   random_state=0,
                   max_iter=ITERATIONS).fit(activities)
    print(kmean.cluster_centers_)
    print(neurons)
    clustered_matrix_a = clusterise(activities, kmean.cluster_centers_)
    print(clustered_matrix_a)
    clustered_matrix_b = clusterise(x, neurons)
    print(clustered_matrix_b)


    joint = np.zeros([len(neurons), N_CLUSTERS], dtype = np.int)
    for index in range(len(x)):
        i = clustered_matrix_b[index]
        j = clustered_matrix_a[index]
        joint[i, j] += 1
    joint = np.true_divide(joint, sum(sum(joint)))
    print (joint.round(2))

    r = x[np.random.randint(len(x))]
    trajectory = [r]
    for t in range(100):
        s = getCluster(r, neurons)
        a = kmean.cluster_centers_[policy(joint, s)]
        r = np.add(r, a)
        trajectory.append(r)

    # print ('tr', trajectory)