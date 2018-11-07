# This file provides code which you may or may not find helpful.
# Use it if you want, or ignore it.
import random
import numpy as np


def read_data(fname):
    data = {}
    for line in file(fname):
        arr = line.split()
        data.extend(map(lambda x: x.split('/'), arr))
    return data
