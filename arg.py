# coding: utf-8

# A simple arguments manager written by Tamamu.
# 2016-12-04

import os
import glob

class Arguments:
    """A simple arguments manager."""

    def __init__(self, argv):
        self.cmd = argv[0]
        self.argv = argv[1:]

    def get_as_file(self, num):
        if len(self.argv) <= num:
            return None
        else:
            path = self.argv[num]
            if os.path.exists(path) & os.path.isfile(path):
                return path
            else:
                return None

    def get_as_filelist(self, num):
        if len(self.argv) <= num:
            return None
        else:
            path = self.argv[num]
            if os.path.exists(path) & os.path.isdir(path):
                return glob.glob(path + "/*")
            else:
                return None