# coding: utf-8

from arg import Arguments
from rect import Rectangle
from utils import resize
import contour as C
from contour import recognize_contour
import cv2
import sys
import os

USAGE = """Usage: extract.py imagesdir

Output each fetrures of images.
"""

PRIMITIVE_BORDER = (0, 0, 255)
SKIN_BORDER = (255, 0, 0)
HAIR_BORDER = (0, 255, 0)

BODY_RATIO_THRESHOLD = 1.5

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
body_cascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')


def extract(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = resize(img, 300)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 3)
    if len(faces) <= 0:
        return None

    bodies = body_cascade.detectMultiScale(gray, 1.1, 3)
    if len(bodies) <= 0:
        return None

    face = Rectangle(faces[0][0], faces[0][1], faces[0][2], faces[0][3])
    body = Rectangle(bodies[0][0], bodies[0][1], bodies[0][2], bodies[0][3])

    # Body/Face Section
    body_ratio = body.w / face.w
    if body_ratio <= BODY_RATIO_THRESHOLD:
        return None

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

    # Contour Section
    contour = recognize_contour(img[face.y:face.y2, face.x:face.x2])

    print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(os.path.basename(path), skinR, skinG, skinB, hairR, hairG, hairB, body_ratio, contour))

if __name__ == '__main__':
    arg = Arguments(sys.argv)
    files = arg.get_as_filelist(0)

    # Check the file is exist
    if files is None:
        sys.stderr.write(USAGE)
        exit(1)

    C.ready()
    print("画像\t肌R\t肌G\t肌B\t髪R\t髪G\t髪B\t幅比\t輪郭")
    for file in files:
        extract(file)

    exit(0)
