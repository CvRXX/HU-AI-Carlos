import numpy as np
import weatherMeasurement
from collections import Counter

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

unknownDays = []
for item in days :
	measurment = weatherMeasurement.WeatherMeasurement(*item[1:])
	measurment.setDate(item[0])
	unknownDays.append(measurment)	


def closestNeigbour(trainedSet, datapoint, k):
	closestNeigbours = []
	for measurment in trainedSet:
		distance = datapoint.measureDistance(measurment)
		closestNeigbours.append([measurment.label, distance])
	closestNeigbours.sort(key=lambda x: x[1])
	occurances={}
	for item in closestNeigbours[:k]:
		if item[0] in occurances:
			occurances[item[0]]+=1
		else:
			occurances[item[0]]=1
	return max(occurances, key=occurances.get)

def selectK(trainedSet, validationMeasurementsWithDate, kbegin, kend):
	print("Calculating best k")
	bestk=0
	bestkscore=0
	for k in range(kbegin,kend):
		print (str(k)+"/"+str(kend-kbegin), end="\r")
		right =0 
		for item in validationMeasurementsWithDate:
			if item.label == closestNeigbour(trainedSet,item, k):
				right+=1
		if right>bestkscore:
			bestkscore=right
			bestk=k
	print("best K is: " + str(bestk))
	print("This K has a succesrate of: " + str(bestkscore) + "%!")
	return bestk
bestk = selectK(measurements,validationMeasurementsWithDate,1,101)
print("Using this K to calculate the unknown days:")
for i, point in enumerate(unknownDays):
	print(str(i) + ": " + str(closestNeigbour(measurements,point, bestk)))