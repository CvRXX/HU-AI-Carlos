import pickle ,os
import numpy as np
from pylab import imshow , show , cm
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation

f = open('mnist.pkl', 'rb')
train_set , valid_set , test_set = pickle.load(f, encoding='latin1')
f.close()


getImage2 = lambda x,set : [a for a in  [img[x] for img in set]][0]
getImage3 = lambda x,set : [a for a in  [img[x] for img in set]][1]

trainingX = np.array([getImage2(idx,train_set) for idx in range(0,50000)])
trainingY = np.array([getImage3(idx,train_set) for idx in range(0,50000)])

testX = np.array([getImage2(idx,test_set) for idx in range(0,10000)])
testY = np.array([getImage3(idx,test_set) for idx in range(0,10000)])

model = Sequential()
model.add(Dense(300, activation='sigmoid', input_dim=784,)) # 784 input neurons go in here.
model.add(Dense(300, activation='sigmoid')) # We hope to find parts of the digit here.
model.add(Dense(100, activation='sigmoid')) # We hope to find combination of above parts here.
model.add(Dense(10, activation='sigmoid')) # 10 output nodes for 0-10 digits. 

model.compile(optimizer='rmsprop',
              loss='sparse_categorical_crossentropy', # We use this loss calculation because we want to find classes represented by a number
              metrics=['accuracy'])


model.fit(trainingX, trainingY, epochs=10, batch_size=20)
print(model.evaluate(testX, testY, batch_size=128))
