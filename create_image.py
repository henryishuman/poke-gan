from __future__ import print_function, division

from keras.datasets import mnist
from keras.datasets import cifar10
from keras.layers import Input, Dense, Reshape, Flatten, Dropout
from keras.layers import BatchNormalization, Activation, ZeroPadding2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.convolutional import UpSampling2D, Conv2D
from keras.models import Sequential, Model, load_model
from keras.optimizers import Adam, SGD, RMSprop, Adagrad, Adadelta
import tensorflow as tf

import matplotlib.pyplot as plt
from matplotlib import cm

import sys
import os
from PIL import Image
from glob import glob
import pickle

import numpy as np

def load_generator(data_path):
    return load_model(data_path)

def save_img(generator, output_path, filename):
    noise = np.random.normal(0, 1, (1, 100))
    gen_image = generator.predict(noise)

    im = Image.new('RGB', (gen_image.shape[1], gen_image.shape[2]))

    pixels = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            pixels[i,j] = tuple(gen_image[0, j, i]*255)
    im.save("{}/{}".format(output_path, filename))

def save_img_grid(generator, output_path, filename, rows, cols):
    noise = np.random.normal(0, 1, (rows * cols, 100))
    gen_imgs = generator.predict(noise)

    fig, axs = plt.subplots(rows, cols)
    cnt = 0
    for i in range(rows):
        for j in range(cols):
            axs[i,j].imshow(gen_imgs[cnt, :,:,:])
            axs[i,j].axis('off')
            cnt += 1
    fig.savefig("{}/{}".format(output_path, filename))
    plt.close()

generator = load_generator('models/generator')
save_img_grid(generator, './test_out/', 'test_out_grid.jpg', 5, 5)

for i in range(25):
    save_img(generator, './test_out/', 'test_out_{}.jpg'.format(i+1))