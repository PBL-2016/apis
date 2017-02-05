# coding: utf-8

# A simple rectangle data class written by Tamamu.
# 2016-12-04


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = x+w
        self.y2 = y+h
        self.half_w = int(w/2)
        self.half_h = int(h/2)
        self.quarter_w = int(w/4)
        self.quarter_h = int(h/4)
