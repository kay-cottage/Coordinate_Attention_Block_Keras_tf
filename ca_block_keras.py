from keras.models import Sequential
from keras.layers import Dense,Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
import keras

import keras.backend.tensorflow_backend as K
from keras.layers import * 
import numpy as np

def CoordAtt(x):
    h = x.shape[0]
    w = x.shape[1]
    c = x.shape[2]
    inputTensor = Input((h, w, c))

    pool_h = MaxPooling2D(pool_size=(1,h))(inputTensor)
    pool_w = MaxPooling2D(pool_size=(w,1))(inputTensor)
    pool_h = K.permute_dimensions(pool_h, (0, 2, 1, 3))

    y = Concatenate(axis=2)([pool_h, pool_w])

    mip = max(8, 32 // 32)
    y = K.squeeze(y, axis=1)
    y = Conv1D(mip, kernel_size=1, strides=1, padding='VALID')(y)
    y = BatchNormalization()(y)
    y = Activation('sigmoid')(y)

    x_h, x_w = y[:, 0:299, :], y[:, 299:, :]

    y_h = Conv1D(c, kernel_size=1, strides=1, padding='VALID')(x_h)
    y_h = Activation('sigmoid')(y_h)
    y_h = K.expand_dims(y_h, axis=2)
    y_w = Conv1D(c, kernel_size=1, strides=1, padding='VALID')(x_w)
    y_w = Activation('sigmoid')(y_w)
    y_w = K.expand_dims(y_w, axis=1)

    y = y_h*y_w*a
    return y
