import tensorflow as tf

from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model

import numpy as np

class alphaZero(Model):
  def __init__(self):
    super(alphaZero, self).__init__()
    self.conv1 = Conv2D(32, 3, activation='relu', padding='same')
    self.conv2 = Conv2D(64, 3, activation='relu', padding='same')
    self.conv3 = Conv2D(128, 3, activation='relu')
    self.flatten = Flatten()
    #self.mpl=Dense(512, activation='relu')
    #Priors branch 
    self.priors = Dense(4, activation='softmax')
    self.value = Dense(1, activation='tanh')

  def call(self, x):
    x = self.conv1(x)
    x = self.conv2(x)
    x = self.conv3(x)
    x = self.flatten(x)
    priors = self.priors(x)
    value=self.value(x)
    return priors, value

model = alphaZero()

loss_value = tf.keras.losses.MeanSquaredError()
loss_priors = tf.keras.losses.BinaryCrossentropy()

train_loss_value = tf.keras.metrics.Mean(name='train_loss_value')
train_loss_priors = tf.keras.metrics.Mean(name='train_loss_priors')
train_tot_loss = tf.keras.metrics.Mean(name='train_tot_loss')

optimizer = tf.keras.optimizers.Adam()

@tf.function
def train_step(image, labelValue, labelPriors):
  with tf.GradientTape() as tape:
    priors, value = model(image)
    loss1 = loss_value(labelValue, value)
    loss2 = loss_priors(labelPriors, priors)
    tot_loss=loss1+loss2
  gradients = tape.gradient(tot_loss, model.trainable_variables)
  optimizer.apply_gradients(zip(gradients, model.trainable_variables))
  
  train_loss_value(loss1)
  train_loss_priors(loss2)
  train_tot_loss(tot_loss)


inputData=np.random.random(size=(10,3,3,8))
labelData=np.random.random(size=(10,1))

labelData2=[]
for i in range(10):
  priors=np.zeros(4)
  idx=np.random.randint(0,4)
  priors[idx]=1
  labelData2.append(priors)

labelData2=np.asarray(labelData2)
#out=model(inputData)
'''
value is a number between -1 and 1.
1 means that the board lead to win the game, 
-1 means that the board loads to loose the game (solution not found in the next 100 moves)
the error function is simply a MSE (label_res - value_pred)**2

priors are 4 numbers where the sum of them is 1.
the error is a Xentropy between ther priors and the 
move actually made
'''

for i in range(100):
    train_step(inputData, labelData, labelData2)