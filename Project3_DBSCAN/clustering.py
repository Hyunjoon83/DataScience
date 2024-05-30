import sys
import math

UNVISITED = 0
NOISE = -1

def get_distance(data, p1, p2):
    distance = 0
    for i in range(len(data[0])):
        distance += (data[p2][i] - data[p1][i]) ** 2
    return math.sqrt(distance)

def get_neighbors(data, p, epsilon):
    neighbors = []
    for o in range(len(data)):
        if o != p:
            if get_distance(data, p, o) <= epsilon:
                neighbors.append(o)
        else:
            continue
    return neighbors

def DBSCAN(data, epsilon, minPts):
    cluster_id = 0
    labels = [UNVISITED] * len(data)
    
    for p in range(len(data)):
        if labels[p] == UNVISITED:
            neighbors = get_neighbors(data, p, epsilon)
            
            if len(neighbors) <= minPts:
                labels[p] = NOISE
            else:
                cluster_id += 1
                labels[p] = cluster_id
                
                i = 0
                while i < len(neighbors):
                    q = neighbors[i]
                    if labels[q] == UNVISITED:
                        labels[q] = cluster_id
                        new_neighbors = get_neighbors(data, q, epsilon)
                        
                        if len(new_neighbors) >= minPts:
                            neighbors.extend(new_neighbors)
                            
                    if labels[q] == NOISE:
                        labels[q] = cluster_id
                        
                    i += 1
    return labels
                
            
def read_data(file_name):
    data = []
    with open(file_name, 'r') as input_file:
        for line in input_file:
            parts = line.strip().split('\t')
            x, y = float(parts[1]), float(parts[2])
            data.append((x, y))
    return data

def write_output(filename, labels, n):
    clusters = dict()
    for idx, label in enumerate(labels):
        if label > 0:
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(idx)
    
    sorted_clusters = sorted(clusters.values(), key=len, reverse=True)
    
    for i in range(n):
        with open(f"{filename}_cluster_{i}.txt", 'w') as output_file:
            if i < len(sorted_clusters):
                for obj_id in sorted_clusters[i]:
                    output_file.write(f"{obj_id}\n")
            else:
                output_file.write("")

def main():
    filename = sys.argv[1]  # input file name
    n = int(sys.argv[2])  # number of clusters
    epsilon = float(sys.argv[3])  # maximum radius of the neighborhood
    minPts = int(sys.argv[4])  # minimum number of points in an Eps-neighborhood

    data = read_data(filename)
    labels = DBSCAN(data, epsilon, minPts)
    
    write_output(filename.split('.')[0], labels, n)

if __name__ == '__main__':
    main()
