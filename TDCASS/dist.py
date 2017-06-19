#!/usr/bin/env/python3
def dist(lon1, lat1, lon2, lat2):
	import numpy as np
	Rt =  6371008
	d = np.sqrt(((lon1-lon2)*np.cos((lat1+lat2)/2/180*np.pi))**2 + (lat1-lat2)**2)/180*np.pi*Rt
	return d

def totalDist(polyline):
	totalDist = 0
	for i in range(0, (len(polyline)-1)):
		lon1 = polyline[i][0]
		lat1 = polyline[i][1]
		lon2 = polyline[i+1][0]
		lat2 = polyline[i+1][1]
		totalDist = totalDist + dist(lon1, lat1, lon2, lat2)
	return totalDist

#print(dist(0,48,0,49))

#print("total dist")
#print(totalDist([[-8.618643,41.141412],[-8.618499,41.141376],[-8.620326,41.14251]]))

