import numpy as np
import weatherMeasurement
from collections import Counter
import random
import matplotlib.pyplot as pyplot

data = np.genfromtxt('dataset1.csv', delimiter=';', usecols=[0,1,2,3,4,5,6,7], converters={5: lambda s: 0 if s == b"-1" else float(s), 7: lambda s: 0 if s == b"-1" else float(s)})
validationData = np.genfromtxt('validation1.csv', delimiter=';', usecols=[0,1,2,3,4,5,6,7], converters={5: lambda s: 0 if s == b"-1" else float(s), 7: lambda s: 0 if s == b"-1" else float(s)})
days = np.genfromtxt('days.csv', delimiter=';', usecols=[0,1,2,3,4,5,6,7], converters={5: lambda s: 0 if s == b"-1" else float(s), 7: lambda s: 0 if s == b"-1" else float(s)})

measurements = []
for item in data :
	measurment = weatherMeasurement.WeatherMeasurement(*item[1:])
	measurment.setDate(item[0])
	measurements.append(measurment)

validationMeasurementsWithoutDate = []
for item in validationData :
	validationMeasurementsWithoutDate.append(weatherMeasurement.WeatherMeasurement(*item[1:]))

validationMeasurementsWithDate = []
for item in validationData :
	measurment = weatherMeasurement.WeatherMeasurement(*item[1:])
	measurment.setDate(item[0])
	validationMeasurementsWithDate.append(measurment)

def kmeans(dataset,k):
	centroids = random.sample(dataset, k)
	
	hasSomethingChanged = 1
	for run in range(0,10000):
		if hasSomethingChanged == 0:
			break
		hasSomethingChanged = 0

		centroidSums = [weatherMeasurement.WeatherMeasurement(0,0,0,0,0,0,0)] * k
		centroidNumberOfItems = [0] * k
		# Find the closest centroid for each item in the dataset and assign it to the item.
		for item in dataset:
			closestCentroid = 0
			closestCentroidDistance = centroids[0].measureDistance(item)
			for idx, centroid in enumerate(centroids[1:]):
				distance = centroid.measureDistance(item)
				if distance < closestCentroidDistance:
					closestCentroid = idx+1
					closestCentroidDistance = distance
			if item.centroid != closestCentroid:
				hasSomethingChanged+=1
				item.centroid = closestCentroid
			centroidSums[closestCentroid]+=item
			centroidNumberOfItems[closestCentroid]+=1


		for centroidIdx, centroidSum in enumerate(centroidSums):
			if centroidNumberOfItems[centroidIdx]:
				centroids[centroidIdx] = weatherMeasurement.WeatherMeasurement(
					centroidSum.fg/centroidNumberOfItems[centroidIdx],
					centroidSum.tg/centroidNumberOfItems[centroidIdx],
					centroidSum.tn/centroidNumberOfItems[centroidIdx],
					centroidSum.tx/centroidNumberOfItems[centroidIdx],
					centroidSum.sq/centroidNumberOfItems[centroidIdx],
					centroidSum.dr/centroidNumberOfItems[centroidIdx],
					centroidSum.rh/centroidNumberOfItems[centroidIdx])
	return(centroids,dataset)


def calculateDistance(centroids,dataset):	
	centroidSum=0
	for idx, centroid in enumerate(centroids):
		for item in dataset:
			if idx == item.centroid:
				centroidSum+=item.measureDistance(centroids[idx])

	return centroidSum

def findCentroidLabels(centroids,dataset):
	for idx, centroid in enumerate(centroids):
		labels = {}
		for item in dataset:
			if idx == item.centroid:
				if item.label in labels:
					labels[item.label]+=1
				else:
					labels[item.label]=1
		

		centroid.label=max(labels, key=labels.get)
	return centroids, dataset





def findBestK(dataset, maxK, runs):
	kScores = []
	for k in range(2,maxK+1):
		sum = []
		for run in range(1,runs+1):
			print("Finding best K: " + str(k) + "/" + str(maxK) + " run: " + str(run) + "/" + str(runs) + "              ", end="\r")
			centroids, dataset = kmeans(dataset,k)
			sum.append(calculateDistance(centroids,dataset))
		kScores.append(max(sum))
	pyplot.scatter(range(2,maxK+1),kScores,label='Scatter Plot 1',color='r')
	pyplot.show()
	return kScores	

def validateLabels(dataset, k):
	good = 0
	false = 0
	centroids, dataset = findCentroidLabels(*kmeans(dataset,k))
	for idx, centroid in enumerate(centroids):
		for item in dataset:
			if item.centroid == idx:
				if item.label == centroid.label:
					good+=1
				else:
					false+=1
	print("Good: " + str(good))
	print("False: " + str(false))
	print("That's: " + str(round(good/((false+good)/100 )) ) + "%!")




findBestK(measurements, 10, 500)
# From the graph I can tell the best K is: 3!
validateLabels(measurements,3)
# I can validate around 50% of the labels correctly. 
# This is not so bad if you compare this 
# to k-neigbours which should be better at this!

