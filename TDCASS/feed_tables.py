#!/usr/bin/env/python3

from cassandra.cluster import Cluster

import csv
import IPython
import dist
import simplejson as JSON
import datetime
from cassandra.query import BatchStatement



cluster = Cluster()
session = cluster.connect('e32')
# make cassandra understand tuple python type
session.encoder.mapping[tuple] = session.encoder.cql_encode_tuple


id = 0
k =0
# Loop in main file
with open('/train.csv', 'rt') as csvfile:
	firstRow = True

	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	batch = BatchStatement()
	n =1
	BATCH_SIZE = 40
	for row in reader:
		k += 1
		if firstRow :
			firstRow = False
		else :	
			try: 
				trip = row[0]
				timestamp = row[5]
				taxi = row[4]
				polyline = JSON.loads(row[8])
					
				if timestamp and len(polyline) > 2 :
					# parsing date
					annee = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y')
					mois = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%m')
					jour = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d')
					heure = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%H')
					minute = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%M')
					dayOWeek = datetime.datetime.fromtimestamp(int(timestamp)).weekday()	
					
					
					# parsing polyline and calcul distances
					origin = polyline[0]
					destination = polyline[-1]
					originLon = round(origin[0],2)
					originLat = round(origin[1],2)
					destinationLon = round(destination[0],2)
					destinationLat = round(destination[1],2)
					distance = dist.totalDist(polyline)
					

					# feed trip_by_time
					reqA = "insert into TRIP_BY_TIME (annee, mois, jour, dayOWeek, heure, minute, trip, distance, o_lon, o_lat, d_lon, d_lat) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (str(annee), str(mois), str(jour), str(dayOWeek), str(heure), str(minute), str(trip), str(distance), str(originLon), str(originLat), str(destinationLon), str(destinationLat))			

					# feed trip_by_origin_area
					reqC = "insert into TRIP_BY_ORIGIN_AREA (o_lon, o_lat, trip, dayOWeek, heure, distance) values ('%s', '%s', '%s', '%s', '%s', '%s');" % (str(originLon), str(originLat), str(trip), str(dayOWeek), str(heure), str(distance))

					# feed trip_by_destination_area
					reqD = "insert into TRIP_BY_DESTINATION_AREA (d_lon, d_lat, trip, dayOWeek, heure, distance) values ('%s', '%s', '%s', '%s', '%s', '%s');" % (str(originLon), str(originLat), str(trip), str(dayOWeek), str(heure), str(distance))
					
					# feed trip_by_origin_and_destination
					reqE = "insert into TRIP_BY_ORIGIN_AND_DESTINATION (o_lon, o_lat, d_lon, d_lat, trip, dayOWeek, heure, distance) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (str(originLon), str(originLat), str(destinationLon), str(destinationLat), str(trip), str(dayOWeek), str(heure), str(distance))
					
					if taxi :
						# feed trip_by_taxi
						reqB = "insert into TRIP_BY_TAXI (taxi, trip, dayOWeek, heure, distance, o_lon, o_lat, d_lon, d_lat) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (str(taxi), str(trip), str(dayOWeek), str(heure), str(distance), str(originLon), str(originLat), str(destinationLon), str(destinationLat))
					
					else : 
						reqB = None
				else : 
					reqA = None
					reqC = None
					reqD = None
					reqE = None
						
						
				# batching session query
				if n%BATCH_SIZE == 0 :
					n = 1
					session.execute(batch)
					print(k)
					batch = BatchStatement()
				else :
					n += 1
					if reqA :
						batch.add(reqA)
					if reqB :
						batch.add(reqB)
					if reqC :
						batch.add(reqC)
					if reqD :
						batch.add(reqD)
					if reqE :
						batch.add(reqE)
			
			
	
			except:
				IPython.embed()
				break


#session.execute(reqA, timeout = 18)
							

