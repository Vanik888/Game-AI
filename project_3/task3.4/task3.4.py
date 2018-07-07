import logging
import sys
import csv
import numpy as np
from sklearn.cluster import KMeans
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patheffects as path_effects

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(asctime)s | %(message)s',
                    datefmt="%H:%M:%S")

logger = logging.getLogger('Logger from Task 2.2')



SHOW_PLOTS = False
N_CLUSTERS = [10, 60]


class PATHS:
    path1 = 'path1'
    path2 = 'path2'


class N_CLUSTERS:
    n60 = 60
    n10 = 10


class NEURONS_FILE:
    n10 = 'neurons_10.csv'
    n60 = 'neurons_60.csv'


class ITERATIONS:
    n1000 = 1000
    n10000 = 10000


USER_STATE_FILE = 'q3dm1.csv'
TRAJECTORY_PLOT_FILE = 'trajectory.png'
KMEAN_PLOT_FILE = 'a_kmean.png'
SOM_PLOT_FILE = 'x_som.png'


def get_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
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
            if dist < np.linalg.norm(d-clusters[mapping_array[i]]):
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
    return ind


def jointProbabilities(x, activities, neurons, kmean):
    joint = np.zeros([len(neurons), len(kmean.cluster_centers_)], dtype=np.int)
    for index in range(len(x)):
        i = getCluster(x[index], neurons)
        j = getCluster(activities[index], kmean.cluster_centers_)
        joint[i, j] += 1

    logger.debug('Joint probabilities \n %s' % joint)

    def _normilize(row):
        sum = np.sum(row, dtype=float)
        row = row / sum if sum != 0 else row
        return row

    jointNorm = np.apply_along_axis(_normilize, axis=1, arr=joint)
    logger.info('Normailized joint probabilities\n %s' % jointNorm.round(2))

    return jointNorm


def computeTrajectory(iterations, x, neurons, kmean, joint):
    starting_index = np.random.randint(len(x))
    r = x[starting_index]
    logger.debug('Trajectory start point=%s' % r)
    trajectory = [r]
    for t in range(iterations):
        s = getCluster(r, neurons)
        # print s
        # print policy(joint, s)
        a = kmean.cluster_centers_[policy(joint, s)]
        # print a
        r = np.add(r, a)
        # print r
        trajectory.append(r)

    trajectory = np.matrix(trajectory)
    # print (starting_index)
    return trajectory


def plot_clusters(data, clusters_map, centers, plot_name='3dplot.png'):
    global SHOW_PLOTS
    fig = plt.figure()
    fig.set_size_inches(5.5, 4.5)
    ax = fig.add_subplot(111, projection='3d')
    join_data_cluster = np.append(data, clusters_map, axis=1)

    colors = cm.rainbow(np.linspace(0, 1, len(centers)))
    for i, c in zip(xrange(len(centers)), colors):
        d = join_data_cluster[join_data_cluster[:, -1] == i]
        if d.size > 0:
            t = ax.text(centers[i][0], centers[i][1], centers[i][2], i, color=c)
            t.set_path_effects(
                [path_effects.Stroke(linewidth=3, foreground='black'),
                 path_effects.Normal()])
            ax.scatter(d[:, 0], d[:, 1], d[:, 2],  c=c)

    ax.set_xlim(left=np.min(data[:, 0]), right=np.max(data[:, 0]))
    ax.set_ylim(bottom=np.min(data[:, 1]), top=np.max(data[:, 1]))
    ax.set_zlim(bottom=np.min(data[:, 2]), top=np.max(data[:, 2]))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    file_path = plot_name
    plt.savefig(file_path, facecolor='w', edgecolor='w',
                papertype=None, format='png', transparent=False,
                pad_inches=0.1, dpi=100)
    if SHOW_PLOTS:
        plt.show()


def plot_trajectory(trajectory, plot_name):
    global SHOW_PLOTS
    x = np.append([], trajectory[:, 0])
    y = np.append([], trajectory[:, 1])
    z = np.append([], trajectory[:, 2])
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(x, y, z, label='trajectory')
    file_path = plot_name
    plt.savefig(file_path, facecolor='w', edgecolor='w',
                papertype=None, format='png', transparent=False,
                pad_inches=0.1, dpi=100)
    if SHOW_PLOTS:
        plt.show()


def analyze(path, user_state_file, neurons_state_file, n_clusters, iterations):
    logger.info('\nPATH=%s\nStart analysis with:'
                '\nn_clusters=%s'
                '\niterations=%s'
                '\nneurons_file=%s\n' % (path, n_clusters, iterations,
                                         neurons_state_file))

    def _get_file_name(filename, prefix=path):
        return '%s/%s' % (prefix, filename)

    user_state_file = _get_file_name(user_state_file)
    neurons_state_file = _get_file_name(neurons_state_file)
    plots_dir = _get_file_name('plots')


    x = get_data(user_state_file)
    neurons = get_data(neurons_state_file)
    activities = get_activities(user_state_file)
    kmean = KMeans(n_clusters=n_clusters,
                   random_state=0,
                   max_iter=iterations).fit(activities)
    print 'kmeans\n', (kmean.cluster_centers_)
    print 'neurons\n', (neurons)

    clustered_matrix_a = clusterise(activities, kmean.cluster_centers_)
    clustered_matrix_x = clusterise(x, neurons)
    logger.debug('clustered a\n %s' % clustered_matrix_a)
    logger.debug('clustered x\n %s' % clustered_matrix_x)

    def _get_plots_name(filename, plots_dir=plots_dir, n_neurons=len(neurons),
                        n_clusters=len(kmean.cluster_centers_), prefix=path):
        return '%s/%scl_%sn_%siter_%s' % (plots_dir, n_clusters, n_neurons,
                                          iterations, filename)

    som_plot_file = _get_plots_name(SOM_PLOT_FILE)
    kmean_plot_file = _get_plots_name(KMEAN_PLOT_FILE)
    trajectory_plot_file = _get_plots_name(TRAJECTORY_PLOT_FILE)

    plot_clusters(activities, clustered_matrix_a, kmean.cluster_centers_, kmean_plot_file)
    plot_clusters(x, clustered_matrix_x, neurons, som_plot_file)

    joint = jointProbabilities(x, activities, neurons, kmean)#, clustered_matrix_x, clustered_matrix_a)
    print joint.round(2)
    trajectory = computeTrajectory(400, x, neurons, kmean, joint)
    plot_trajectory(trajectory, trajectory_plot_file)
    logger.info('Analysis is done!')


if __name__ == '__main__':
    # # ANALYSIS FOR PATH 1
    # analyze(PATHS.path1, USER_STATE_FILE,
    #         NEURONS_FILE.n10,
    #         N_CLUSTERS.n10,
    #         ITERATIONS.n10000)
    #
    # analyze(PATHS.path1, USER_STATE_FILE,
    #         NEURONS_FILE.n10,
    #         N_CLUSTERS.n60,
    #         ITERATIONS.n10000)
    #
    # analyze(PATHS.path1, USER_STATE_FILE,
    #         NEURONS_FILE.n60,
    #         N_CLUSTERS.n60,
    #         ITERATIONS.n10000)

    # ANALYSIS FOR PATH 2

    analyze(PATHS.path2, USER_STATE_FILE,
            NEURONS_FILE.n10,
            N_CLUSTERS.n10,
            ITERATIONS.n10000)

    analyze(PATHS.path2, USER_STATE_FILE,
            NEURONS_FILE.n10,
            N_CLUSTERS.n60,
            ITERATIONS.n10000)

    analyze(PATHS.path2, USER_STATE_FILE,
            NEURONS_FILE.n60,
            N_CLUSTERS.n60,
            ITERATIONS.n10000)


