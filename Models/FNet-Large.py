# -*- coding: utf-8 -*-
"""ForensicNet.ipynb

Automatically generated by Colaboratory.
"""

!pip install tensorflow-addons

# Commented out IPython magic to ensure Python compatibility.
import os
from tensorflow.keras.layers import Input, Dense, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Dropout, Reshape, Concatenate, LeakyReLU
from tensorflow.keras.models import Model
#import necessary libraries
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, utils
import tensorflow_addons as tfa

import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
from tensorflow.keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping

import numpy as np 
import pandas as pd 
import glob
from sklearn.model_selection import train_test_split
from sklearn import metrics
import cv2
import seaborn as sns
import matplotlib.pyplot as plt2
from keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.optimizers import RMSprop, Adam, SGD
from keras import regularizers
from keras.callbacks import CSVLogger, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

"""**Model Architecture**"""

def real_block(input, dim, drop_path=0.0):
     
     #shortcut connection
      shortcurt = input 
      x = layers.Conv2D(filters=dim, kernel_size=7, padding='same', groups=dim)(input)
      x = layers.LayerNormalization(epsilon=1e-6)(x)

      x = layers.Dense(4 * dim)(x)
      x = layers.BatchNormalization()(x)
      x = layers.ReLU()(x)
      x = layers.Dense(dim)(x)
      #Stochastic depth
      drop_depth = tfa.layers.StochasticDepth(drop_path) if drop_path > 0.0 else layers.Activation("linear")

      output = layers.Add()([shortcurt, drop_depth(x)])

      return output

def stem(input, dim):

  x = layers.Conv2D(filters=dim, kernel_size=4, strides=4)(input)
  x = layers.BatchNormalization()(x)

  return x

def downsampling_layers(input, dim):

#   x = layers.LayerNormalization(epsilon=1e-6)(input)
  x = layers.BatchNormalization() (input)
  x = layers.Conv2D(filters=dim, kernel_size=2, strides=2)(x)

  return x

def real_model(input_shape=(224, 224, 3), dims=[128, 256, 512, 1024], num_classes=2):

  input = layers.Input(input_shape)

  # stem
  x = stem(input, dims[0])

  # Stage 1 x3, dim[0] = 64
  for _ in range(3):
    x = real_block(x, dims[0])

  # Downsampling Block + stage 2 x3, dim[1] = 128
  x = downsampling_layers(x, dims[1])
  for _ in range(3):
    x = real_block(x, dims[1])

  # Downsampling Block + stage 3 x7, dim[2] = 256
  x = downsampling_layers(x, dims[2])
  for _ in range(9):
    x = real_block(x, dims[2])

  # Downsampling Block + stage 4 x3, dim[3] = 512
  x = downsampling_layers(x, dims[3])
  for _ in range(3):
    x = real_block(x, dims[3])
    
  # Classification head: Global average pool + layer norm + fully connected layer
  x = layers.GlobalAvgPool2D()(x)

  x = layers.LayerNormalization(epsilon=1e-6)(x)    
  x = layers.Dense(units= dims[3], activation='relu') (x)
  x = layers.Dropout(0.2) (x)
  output = layers.Dense(units=num_classes, activation='softmax')(x)

  model = keras.Model(input, output, name='FNet')

  return model

model= real_model()
model.summary()

"""**Training Model**"""

epochs = 50
batch_size = 100
init_lr = 1e-5
optimizer = Adam(lr = init_lr, decay = init_lr/epochs)


model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics = ['accuracy'])

