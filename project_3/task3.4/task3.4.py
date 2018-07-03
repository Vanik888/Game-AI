import csv
import numpy as np
from sklearn.cluster import KMeans

N_CLUSTERS = 10
ITERATIONS = 1000

def get_data():
    with open('q3dm1-path1.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        data = [i for i in reader]
        return np.array(data, dtype=np.float)


def get_activities():
    data = get_data()
    activities = np.full([len(data)-1, 3], -1, dtype=np.float)
    for i in range(len(data)-1):
        activities[i] = data[i+1] - data[i]
    return activities


if __name__ == '__main__':
    activities = get_activities()
    kmean = KMeans(n_clusters=N_CLUSTERS,
                   random_state=0,
                   max_iter=ITERATIONS).fit(activities)
    print(kmean.cluster_centers_)
