import math


class Neuron(object):

	inputs = []
	weights = []
	isOutputNode = False
	delta = 0
	error = 0
	value = 0


	def __init__(self, inputs, weights, isOutputNode):
		self.inputs = inputs
		self.weights = weights
		self.isOutputNode = isOutputNode

	# Updating the value manualy so it only has to be done once in training.
	def updateValue(self):
		value = 0
		for weight, node in zip(self.weights,self.inputs):
			value += node.getValue() * weight
		self.value = self.sigmoid(value)

	def getValue(self):
		return self.value

	def sigmoid(self, x):
 		return 1 / (1 + math.exp(-x))

	def updateDelta(self, desiredActivation=0):
		summedInput = 0
		for weight, node in zip(self.weights,self.inputs):
			summedInput += weight * node.getValue()
			
		if self.isOutputNode:
			self.delta = (self.sigmoid(summedInput) * (1-self.sigmoid(summedInput))) * (desiredActivation - self.getValue())
		else:
 			self.delta = (self.sigmoid(summedInput) * (1-self.sigmoid(summedInput))) * self.error

		for idx, (weight, node ) in enumerate(zip(self.weights,self.inputs)):
			if node.inputs:
 				self.inputs[idx].error += (weight * self.delta )

	def updateWeights(self,learningRate=0.1):
		newWeights = []
		for weight, node in zip(self.weights,self.inputs):
			newWeights.append( weight + (learningRate * node.getValue() * self.delta))
		self.weights = newWeights
		self.delta = 0
		self.error = 0


class InputNeuron(object):
	"""docstring for Neuron"""
	inputs = None
	value = None

	def __init__(self, value):
		self.value = value
	def getValue(self):
		return self.value
	def setValue(self, value):
		if (value) > 1:
			raise MemoryError("input is bigger than one")
		self.value = value