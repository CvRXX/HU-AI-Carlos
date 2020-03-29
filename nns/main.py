import random
import csv
import network
import time

def getIrisData(filePath):
	# Get the csv
	with open(filePath, newline='') as f:
	    reader = csv.reader(f)
	    data = list(reader)

	# Make sure the values are between 0-1 for the sigmoid function.
	for item in data:
		item[0] = float(item[0])/10
		item[1] = float(item[1])/10
		item[2] = float(item[2])/10
		item[3] = float(item[3])/10

	# Add numerical indicators for the classes.
	for item in data:
		if item[4] == 'Iris-setosa':
			item.append(1)
			item.append(0)
			item.append(0)
		if item[4] == 'Iris-versicolor':
			item.append(0)
			item.append(1)
			item.append(0)	
		if item[4] == 'Iris-virginica':
			item.append(0)
			item.append(0)
			item.append(1)	

	# Shuffle the data
	random.shuffle(data)

	# Return a testset that is 10% of the total. The rest is for training.
	testSet = data[:int(len(data)*0.10)]
	trainSet = data[int(len(data)*0.10):]
	return (trainSet, testSet)

(trainSet, testSet) = getIrisData('iris.data')

for run in range(0,5):
	neuralNetwork = network.Network()

	print("Generating a network...")
	# I've chosen for a network of 2 hidden layers with a n of nInputLayers. 
	# This is mainly because I got good results on this.
	neuralNetwork.generate(4,3,2)
	print("The following network has been generated:")
	print(neuralNetwork)

	print("Starting training...")
	neuralNetwork.trainNetwork(trainSet,1,0.000001)
	print("Training finished!")
	print("Starting testing...")
	correctlyDetected = round(neuralNetwork.test(testSet),2)
	print("The network detected " + str(correctlyDetected) + "%  of the testset correctly!") 													
	if correctlyDetected<60:
		print("Local minimum detected, running the program again to mitgate...")
		print("Waiting a bit for new randomness...")
		print()
		time.sleep(3)
	else:
		exit()
print("Something went wrong. Multiple tries of avoiding a local minimum have failed.")