from cassandra.cluster import Cluster

import numpy as np
import simplejson as JSON
import math

# vector c = [ 
    # {(olon, olat, dlon, dlat), n1}, 
    # {(olon, olat, dlon, dlat), n2}, 
    # {(olon, olat, dlon, dlat), n3}
# ]

# intialisation random : take 5 random points - a travers toute la table

    # pour chaque row de table
        # trouver k en calulant distMin(row, c)
        # met à jour le center du clusters k avec ck = ((nk*ck) + (olon', olat', dlon', dlat')) / (nk + 1)
        # sauver l'information ci,k dans list des labels


cluster = Cluster()
session = cluster.connect('e32')
K = 5

class Cluster:
    def __init__(self, value):
        self.value = value
        self.olon = 0
        self.olat = 0
        self.dlon = 0
        self.dlat = 0
        self.done = False
        self.nk = 0
    
    # estimate 4d euclidian distance
    def distFrom(self, olon, olat, dlon, dlat):
        return math.sqrt(math.pow((self.olon - olon),2) + math.pow((self.olat - olat),2) + math.pow((self.dlon - dlon),2) + math.pow((self.dlat - dlat),2))
    
    # move centroid according to new points
    def fitCentroid(self, olon, olat, dlon, dlat):
        self.nk +=1
        self.olon = ( ((self.olon*self.nk) + olon) / (self.nk + 1) )
        self.olat = ( ((self.olat*self.nk) + olat) / (self.nk + 1) )
        self.dlon = ( ((self.dlon*self.nk) + dlon) / (self.nk + 1) )
        self.dlat = ( ((self.dlat*self.nk) + dlat) / (self.nk + 1) )

    def printCluster(self):
        print("cluster "+ str(self.value) + " : \n" + " - origin(" + str(self.olon) + "," + str(self.olat) + ")\n" + " - destination(" + str(self.dlon) + "," + str(self.dlat) + ")\n")



# compare all 4d distance and return closest centroids'index
def findClosestClusterIndex(clusters, olon, olat, dlon, dlat):
    minimum = 999999999999
    i = 0
    index = 0
    for cluster in clusters:
        dist = cluster.distFrom(olon, olat, dlon, dlat)
        if  dist < minimum:
            minimum = dist 
            index = cluster.value - 1
    
    return index     

# centroid initialization to 0
clustersArray = []
for count in range(1,K):
	c = Cluster(count)
	clustersArray.append(c)

# centroids random intialization
def kmeans_initialization(k):
    #n = session.execute("select count(*) from e32.TRIP_BY_ORIGIN_AND_DESTINATION;");
    rows = session.execute("SELECT o_lon, o_lat, d_lon, d_lat FROM e32.TRIP_BY_ORIGIN_AND_DESTINATION;")
    n = 10000    
    i = 0
    nbyK = int(n/K)
    for ck in range(0,K-1):
            row = rows[nbyK]
            clustersArray[ck].olon = float(row.o_lon)
            clustersArray[ck].olat = float(row.o_lat)
            clustersArray[ck].dlon = float(row.d_lon)
            clustersArray[ck].dlat = float(row.d_lat)
            clustersArray[ck].nk += 1
            nbyK += nbyK -1


# centroids models fitting
def kmeans_fit():
    #n = session.execute("select count(*) from e32.TRIP_BY_ORIGIN_AND_DESTINATION;");
    rows = session.execute("SELECT o_lon, o_lat, d_lon, d_lat FROM e32.TRIP_BY_ORIGIN_AND_DESTINATION;")
    
    for row in rows: 
        index = findClosestClusterIndex(clustersArray, float(row.o_lon), float(row.o_lat), float(row.d_lon), float(row.d_lat))
        clustersArray[index].fitCentroid(float(row.o_lon), float(row.o_lat), float(row.d_lon), float(row.d_lat))


# run algorithm
kmeans_initialization(K)
kmeans_fit()

for count in range(0, K-1):
	clustersArray[count].printCluster()


		
		
	
	
