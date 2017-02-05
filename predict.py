# coding: utf-8

from arg import Arguments
from rect import Rectangle
from utils import resize
import contour as C
from contour import recognize_contour
import cv2
import sys

import numpy as np

import chainer
from chainer import Function, gradient_check, Variable, optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

from model import PBLLogi

PRIMITIVE_BORDER = (0, 0, 255)
SKIN_BORDER = (255, 0, 0)
HAIR_BORDER = (0, 255, 0)

P_SUCCESS = 0
P_NOTFOUND = 1
P_UNDETECTED = 2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
body_cascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')

model = None
optimizer = None

def prediction_init():
    init_model()
    C.ready()

def init_model():
    global model, optimizer
    model = PBLLogi()
    optimizer = optimizers.Adam()
    optimizer.setup(model)

    serializers.load_hdf5('pbllogi.model', model)
    serializers.load_hdf5('pbllogi.state', optimizer)

def predict(sr, sg, sb, hr, hg, hb, ratio, contour):
    x = Variable(np.array([[sr/255, sg/255, sb/255, hr/255, hg/255, hb/255, \
        ratio, contour]]).astype(np.float32), volatile='on')
    y = model.fwd(x)
    cluster = np.argmax(y.data[0, :])
    return cluster

def analysis(path):
    # Check the file is exist
    if path is None:
        return (None, P_NOTFOUND)

    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = resize(img, 300)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Face and body detection
    faces = face_cascade.detectMultiScale(gray, 1.1, 3)
    bodies = body_cascade.detectMultiScale(gray, 1.1, 3)
    if len(faces) <= 0 or len(bodies) <= 0:
        return ({"face_detect": len(faces), "body_detect": len(bodies)}, P_UNDETECTED)

    face = Rectangle(faces[0][0], faces[0][1], faces[0][2], faces[0][3])
    body = Rectangle(bodies[0][0], bodies[0][1], bodies[0][2], bodies[0][3])

    # Skin Section
    skinR = skinG = skinB = 0

    for col in range(face.half_w):
        for row in range(10):
            pixel = img[face.y+face.half_h-row+5, face.x+face.quarter_w+col]
            skinB += pixel[0]
            skinG += pixel[1]
            skinR += pixel[2]

    averageDivisor = face.half_w * 10
    skinR = int(skinR / averageDivisor)
    skinG = int(skinG / averageDivisor)
    skinB = int(skinB / averageDivisor)

    # Hair Section
    hairR = hairG = hairB = 0

    top = face.y - 5
    if top < 0:
        top = 0

    for col in range(face.half_w):
        for row in range(10):
            pixel = img[top+row, face.x+face.quarter_w+col]
            hairB += pixel[0]
            hairG += pixel[1]
            hairR += pixel[2]

    hairR = int(hairR / averageDivisor)
    hairG = int(hairG / averageDivisor)
    hairB = int(hairB / averageDivisor)

    # Ratio Section
    body_ratio = body.w / face.w

    # Contour Section
    if C.check_loaded():
        contour = recognize_contour(img[face.y:face.y2, face.x:face.x2])
        if contour == b'circle':
            contour = 0
        elif contour == b'square':
            contour = 1
        elif contour == b'triangle':
            contour = 2
    else:
        contour = 2
#    print('Contour:\t', contour)

    # Prediction
    # Default contour type is 1(square)
    # 0(triangle) and 2(circle)

    cluster = predict(skinR, skinG, skinB, hairR, hairG, hairB, body_ratio, contour)

    return ({"cluster": cluster, "skinR": skinR, "skinG": skinG, "skinB": skinB,
            "hairR": hairR, "hairG": hairG, "hairB": hairB, "ratio": body_ratio,
            "contour": contour}, P_SUCCESS)