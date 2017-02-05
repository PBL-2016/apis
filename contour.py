# coding: utf-8

# Contour recognize function written by Tamamu.
# 2016-12-04


import numpy as np

import chainer
from chainer import cuda
import chainer.functions as F
from chainer.functions import caffe

import cv2

MODEL_PATH = 'caffemodel.binaryproto'
MEAN_PATH = 'mean.npy'
LABEL_PATH = 'labels.txt'

def check_loaded():
    return func != None

def ready():
    global categories
    global mean_image
    global func
#    print('Loading Contour label file...')
    categories = np.loadtxt(LABEL_PATH, str, delimiter='\n')
#    print('Loading Contour mean file...')
    mean_image = np.load(MEAN_PATH)
#    print('Mean shape:', mean_image.shape)
#    print('Loading Contour model file...')
    func = caffe.CaffeFunction(MODEL_PATH)
    return

def recognize_contour(img, gpu=-1):
    in_size = 227

    image = cv2.resize(img, (in_size, in_size))
    image = image.transpose(2, 0, 1)
    image = image.astype(np.float32)
#    print('Image shape:', image.shape)

    def forward(x, t):
        y, = func(inputs={'data': x}, outputs=['fc8_ft'], train=False)
        return F.softmax_cross_entropy(y, t), F.accuracy(y, t)

    def predict(x):
        y, = func(inputs={'data': x}, outputs=['fc8_ft'], train=False)
        return F.softmax(y)

    image -= mean_image

    x_batch = np.ndarray((1, 3, in_size, in_size), dtype=np.float32)
    x_batch[0] = image

    if gpu >= 0:
        x_batch = cuda.to_gpu(x_batch)

    x = chainer.Variable(x_batch, volatile=True)
    score = predict(x)

    if gpu >= 0:
        score = cuda.to_cpu(score.data)

    prediction = list(zip(score.data[0].tolist(), categories))
    prediction.sort(key=lambda x: x[0], reverse=True)
#    for rank, (score, name) in enumerate(prediction, start=1):
#        print('#{0}\t{1}\t{2:>4.1f}'.format(rank, name, score * 100))

    return prediction[0][1]
