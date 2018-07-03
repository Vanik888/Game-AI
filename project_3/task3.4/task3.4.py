import csv
import numpy as np

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
    get_activities()


