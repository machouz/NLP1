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

def dic_to_file(dic, fname):
    data = []
    for key, label in dic.items():
        data.append(key + "\t" + str(label))
    write_to_file(fname, data)

def file_to_dic(fname):
    data = {}
    for line in file(fname):
        key, label = line[:-1].split('\t')
        data[key] = int(label)
    return data


def max_nested_dic(nested_dic):
    maxi = -np.inf
    prev = ''
    current = ''
    for key1, val1 in nested_dic.items():
        for key2, val2 in val1.items():
            if val2 > maxi:
                maxi = val2
                prev = key1
                current = key2
    return prev, current

