from Estimator import *
from datetime import datetime

start = datetime.now()

threshold_unk = 1

fname = "../data/ass1-tagger-train"

estimator = Estimator()


def MLETrain():
    train = read_data(fname)

    for line in train:
        for a, b, c in zip(line, line[1:], line[2:]):
            tag1, tag2, tag3 = a[1], b[1], c[1]
            estimator.addQLine(tag1, tag2, tag3)
            estimator.addELine(a)

        tag2, tag3 = b[1], c[1]
        estimator.addQLine(tag2, tag3)
        estimator.addELine(b)
        estimator.addELine(c)

    estimator.unknown_signature()


if __name__ == '__main__':
    MLETrain()
    q_data = estimator.qFile()
    e_data = estimator.eFile()

    end = datetime.now()
    zman = end - start
    print(zman)
