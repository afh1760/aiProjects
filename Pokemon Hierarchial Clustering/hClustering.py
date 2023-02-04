import numpy as np
import matplotlib.pyplot as plt
import csv
from numpy import linalg as LA
from scipy.cluster import hierarchy

def load_data(filepath):
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        listDict = list()
        for row in reader:
            pokemon = dict()
            key = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
            for x in key:
                pokemon[x] = row[x]
            listDict.append(pokemon)
    return listDict

def calc_features(row):
    x1 = np.int64(row["Attack"])
    x2 = np.int64(row["Sp. Atk"])
    x3 = np.int64(row["Speed"])
    x4 = np.int64(row["Defense"])
    x5 = np.int64(row["Sp. Def"])
    x6 = np.int64(row["HP"])
    stats = np.array([x1,x2,x3,x4,x5,x6])
    return stats

#Helper function
def initializeArray(n, features):
    distArr = np.zeros((n,n))
    for row in range(n):
        for col in range(n):
            distArr[row][col] = LA.norm(features[row]-features[col])
    return distArr

#Helper function
def tiebreaker(i, j):
    x = i[0]
    y = j[0]
    return x,y

def hac(features):
    n = len(features)
    z = np.zeros((n-1, 4))
    
    distArr = initializeArray(n, features)
    for row in range(n-1):
        #Putting into Z
        minDist = np.min(distArr[np.nonzero(distArr)])
        index = np.where(distArr == minDist)
        i = index[0]
        j = index[1]
        
        if len(i) > 1:
            i, j = tiebreaker(i, j)
        
        z[row][0] = i
        z[row][1] = j
        z[row][2] = minDist
        
        if i > (n-1):
            tempI = i - n
            numI = z[tempI][3]
        else:
            numI = 1
        if j > (n-1):
            tempJ = j - n
            numJ = z[tempJ][3]
        else:
            numJ = 1
            
        z[row][3] =  numI+numJ      
        
        #Distance Matrix Remodel
        clusterDist = np.zeros(n+row)
        
        for x in range(n+row):
            clusterDist[x] = np.max((distArr[i][x], distArr[j][x]))
            
        distArr = np.vstack((distArr, clusterDist))
        
        distArrTemp = np.zeros((n+row+1,n+row+1))
        for i1 in range(n+row+1):
            for j1 in range(n+row):
                distArrTemp[i1][j1] = distArr[i1][j1]
        for x in range(n+row):
            distArrTemp[x][n+row] = clusterDist[x]
            
        distArrTemp[i] = 0
        distArrTemp[j] = 0
        distArrTemp[:,i] = 0
        distArrTemp[:,j] = 0
        
        distArr = distArrTemp
    return z

def imshow_hac(Z):
    plt.figure()
    hierarchy.dendrogram(Z)
    plt.show()
    pass