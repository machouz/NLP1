from datetime import datetime
from sys import argv
import os
import sys
from Estimator import *

threshold_unk = 1

fname = argv[1]
qMLE = argv[2]
eMLE = argv[3]



estimator = Estimator()
file = read_data(fname)
train = file[:int(len(file) * 0.9)]
dev = file[len(train):]


def MLETrain():
    for line in train:
        for a, b, c in zip(line, line[1:], line[2:]):
            tag1, tag2, tag3 = a[1], b[1], c[1]
            estimator.addQLine(tag1, tag2, tag3)
            estimator.addELine(a)

        tag2, tag3 = b[1], c[1]
        estimator.addQLine(tag2, tag3)
        estimator.addELine(b)
        estimator.addELine(c)

    for line in dev:
        for a, b, c in zip(line, line[1:], line[2:]):
            tag1, tag2, tag3 = a[1], b[1], c[1]
            estimator.addQLine(tag1, tag2, tag3)
            estimator.addELine(a, dev=True)

        tag2, tag3 = b[1], c[1]
        estimator.addQLine(tag2, tag3)
        estimator.addELine(b, dev=True)
        estimator.addELine(c, dev=True)

    estimator.unknown_signature()



if __name__ == '__main__':
    start = datetime.now()
    MLETrain()
    q_data = estimator.qFile(qMLE)
    e_data = estimator.eFile(eMLE)

    end = datetime.now()
    zman = end - start
    print(zman)
