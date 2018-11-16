# This file provides code which you may or may not find helpful.
# Use it if you want, or ignore it.
import random
import numpy as np


def read_data(fname):
    data = []
    for line in file(fname):
        arr = ['***/STR', '***/STR'] + line[:-1].split()  # Add *** with STR tag at the start and remove the "\n" at EOL
        data.append(map(lambda x: x.rsplit('/', 1), arr))  # Split between word and tag by the last occurrence of "/"
    return data


def write_to_file(fname, data):
    np.savetxt(fname, data, fmt="%s", delimiter='\n')


def file_to_dic(fname):
    data = {}
    for line in file(fname):
        key, label = line[:-1].split('\t')
        data[key] = float(label)
    return data