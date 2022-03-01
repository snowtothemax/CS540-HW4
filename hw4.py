import csv
import numpy as np
from math import inf
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

##Cluster Class##
class Cluster:
    id = -1
    points = set([])
    numPoints = 0

    def __init__(self, id, points, numPoints) -> None:
        self.id = id
        self.points = points
        self.numPoints = numPoints
        pass

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id

    def __hash__(self) -> int:
        return hash(repr(self))

#Loads data in from file. outputs as array of dicts
def load_data(filepath):
    dicts = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            dicts.append(row)
    f.close()

    return dicts

#input a row, return an array better describing the point
def calc_features(row):
    arr = np.array(np.zeros(6), dtype=np.int64)
    arr[0] = int(row["Attack"])
    arr[1] = int(row["Sp. Atk"])
    arr[2] = int(row["Speed"])
    arr[3] = int(row["Defense"])
    arr[4] = int(row["Sp. Def"])
    arr[5] = int(row["HP"])
    return arr

def hac(features):
    clusters = set([Cluster(i,set([i]), 1) for i in range(len(features))])
    Z = []
    newDataset = features
    origLen = len(newDataset)
    distance_matrix = getDistances(features)

    for x in range(origLen-1):
        min = getMinDistance(distance_matrix, clusters)

        # get the matching clusters
        cluster1 = None
        cluster2 = None
        for cluster in clusters:
            if min[1] == cluster.id:
                cluster1 = cluster
            if min[2] == cluster.id:
                cluster2 = cluster
        
        newPoints = cluster1.points.union(cluster2.points)
        newSize = cluster1.numPoints + cluster2.numPoints

        ## get the index that is smaller
        largerInd = cluster1.id if cluster1.id > cluster2.id else cluster2.id
        smallerInd = cluster1.id if cluster1.id < cluster2.id else cluster2.id

        ## add to the thingy
        newCluster = Cluster(origLen + smallerInd, newPoints, newSize)
        Z.append([smallerInd, largerInd, min[0], newCluster.numPoints])

        # remove the clusters and add the new one
        clusters.remove(cluster1)
        clusters.remove(cluster2)
        clusters.add(newCluster)
    
    return np.array(Z)

    
def imshow_hac(Z):
    plt.figure()
    dn = hierarchy.dendrogram(Z)
        


#Represent the data as XY points on a 2D plane
def calcXY(data):
    points = []
    for row in data:
        x = row[0] + row[1] + row[2] #Attack + Sp. Atk + Speed
        y = row[3] + row[4] + row[4] #Defense + Sp. Def + HP
        points.append([x,y])
    return points

#Get the distance matrix for all points
def getDistances(data):
    distance = [[-1 for i in range(len(data))] for j in range(len(data))]
    
    pointsXY = calcXY(data)

    for point in range(len(pointsXY)):
        for point2 in range(len(pointsXY)):
            #check for dupes
            if point == point2: continue
            
            x1,y1 = pointsXY[point][0], pointsXY[point][1]
            x2,y2 = pointsXY[point2][0], pointsXY[point2][1]

            distance[point][point2] = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance

#Get max distance 
def getMinDistance(distances, clusters):
    min = [inf, 0, 0]
    scannedClusters = set([]) #keep track of clusters weve already looked at
    
    #Iterate through clusters and compare points
    for cluster in clusters:
        for clusterComp in clusters:
            scannedClusters.add(cluster.id)

            if clusterComp.id in scannedClusters: continue

            localDist = []
            
            #Iterate through each point in the cluster
            for point in cluster.points:
                for pointComp in clusterComp.points:
                    
                    # add to the list
                    localDist.append(distances[point][pointComp])
            
            ## Check if the distance is a minimum
            dataVal = [max(localDist), cluster.id, clusterComp.id]

            if dataVal[0] < min[0]:
                min = dataVal
            elif dataVal[0] == min[0]:
                if dataVal[1] == min[1]:
                    min = dataVal if dataVal[2] < min[2] else min
                else:
                    min = dataVal if dataVal[1] < min[1] else min
    
    return min