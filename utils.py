# coding: utf-8

# Utility functions written by Tamamu.
# 2016-12-04

import cv2


def color_text(text, r, g, b):
    return "\033[38;2;{0};{1};{2}m{3}".format(r, g, b, text)


def resize(img, size):
    if img.shape[1] < img.shape[0]:
        w = size
        h = int((size/float(img.shape[1]))*img.shape[0])
    else:
        w = int((size/float(img.shape[0]))*img.shape[1])
        h = size
    return cv2.resize(img, (w, h))
