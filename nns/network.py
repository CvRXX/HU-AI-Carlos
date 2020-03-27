import math
import neurons
import random

class Network(object):
	"""docstring for Network"""
	layers = []
	biasses = []

	def __init__(self):
		# self.layers = layers
		pass
	
	def propegateForward(self):
		for layer in self.layers[1:]:
			for neuron in layer:
				neuron.updateValue()

	def propegateBackward(self, desiredActivation):
		# First the outputneurons's deltas are calculated because they
		# require a desired activation.
		for idx, neuron in enumerate(self.layers[-1]):
				neuron.updateDelta(desiredActivation[idx]) 

		# Then update the rest of the delta's in backwards order.
		for layer in reversed(self.layers[1:-1]):
			for neuron in layer:
				neuron.updateDelta()

		# Last update all the weights.
		for layer in self.layers[1:]:
			for neuron in layer:
				neuron.updateWeights()

	def trainNetwork(self, trainingData, learnfactor, endCostDiv, maxEpochs=10000):
		prevcost = 0 
		for i in range(0,maxEpochs):
			singleOutputCosts = []
			totalCost = 0

			for test in trainingData:
				for idx, input in enumerate(self.layers[0]):
					input.setValue(test[idx])

				self.propegateForward()

				for idx, output in enumerate(self.layers[-1]):
					singleOutputCosts.append(math.sqrt(abs(test[5+idx] - output.getValue())))

				self.propegateBackward([test[5],test[6],test[7]])

			for singleOutput in singleOutputCosts:
				totalCost += 1/(2*len(trainingData))*singleOutput

			if abs(totalCost-prevcost) < endCostDiv:
				break
			prevcost = totalCost		


	def test(self, testdata):
		# Test 
		good = []
		for test in testdata:
			for idx, input in enumerate(self.layers[0]):
					input.setValue(test[idx])

			self.propegateForward()
			outputs = []
			for output in self.layers[-1]:
				outputs.append(output.getValue())

			if test[5+outputs.index(max(outputs))]:
				good.append(1)
			else:
				good.append(0)

		return ((sum(good))*100)/len(testdata)

	def generate(self,nInputs,nOutputs,nHiddenLayers):
		self.layers = [[]]
		self.biasses = []

		def generateWeights(nWeights):
			weights = []
			for weight in range(0,nWeights):
				weights.append(random.uniform(0, 1))
			return weights
		# Make inputs:
		for input in range(nInputs):
			self.layers[0].append(neurons.InputNeuron(0))

		# Create hiddenlayers:
		for hiddenLayer in range(1,nHiddenLayers+1):
			self.layers.append([])
			for neuron in range(0,nInputs):
				self.biasses.append(neurons.InputNeuron(1))
				# Generate weights
				weights = generateWeights(len(self.layers[nHiddenLayers-1]))
				neuron = neurons.Neuron(
					self.layers[hiddenLayer-1] + [self.biasses[-1]],
					weights + [0]
					,False)
				self.layers[hiddenLayer].append(neuron)

		# Create outputLayers:
		self.layers.append([])
		for output in range(0,nOutputs):
			self.biasses.append(neurons.InputNeuron(1))
			weights = generateWeights(len(self.layers[:-2]))
			neuron = neurons.Neuron(
					self.layers[-2] + [self.biasses[-1]],
					weights + [0]
					,True)
			self.layers[-1].append(neuron)

	def __str__(self):
		outputString = ""
		for layer in self.layers:
			for neuron in layer:
				if not neuron.inputs:
					outputString += "input     "
				elif neuron.isOutputNode:
					outputString += "output    "
				else:
					outputString += "neuron    "
			outputString += "\n"
		return outputString



	