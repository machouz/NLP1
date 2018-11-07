from utils import *

gamma1 = 0.5
gamma2 = 0.3
gamma3 = 0.2

Q_trigram = {}
Q_bigram = {}
Q_unigram = {}

def QMLE(fname):
    train = read_data(fname)
    Q_trigram = {}
    Q_bigram = {}
    Q_unigram = {}

    for line in train:
        line = map(lambda x: x[1], line)  # Get the only the tags
        for a, b, c in zip(line, line[1:], line[2:]):
            Q_unigram[a] = Q_unigram.get(a, 0) + 1
            Q_bigram[a + " " + b] = Q_bigram.get(a + " " + b, 0) + 1
            Q_trigram[a + " " + b + " " + c] = Q_trigram.get(a + " " + b + " " + c, 0) + 1

        Q_bigram[b + " " + c] = Q_bigram.get(b + " " + c, 0) + 1
        Q_unigram[b] = Q_unigram.get(b, 0) + 1
        Q_unigram[c] = Q_unigram.get(c, 0) + 1

    return Q_unigram, Q_bigram, Q_trigram


def qFile():
    data = []
    for key, label in Q_unigram.items():
        data.append(key + "\t" + str(label))
    for key, label in Q_bigram.items():
        data.append(key + "\t" + str(label))
    for key, label in Q_trigram.items():
        data.append(key + "\t" + str(label))
    write_to_file("q.mle", data)
    return data

def getQ(t1,t2,t3):
    tri = gamma1 * Q_trigram[t1 + " " + t2 + " " + t3]/ Q_bigram[t1 + " " + t2]
    bi = gamma2 * Q_bigram[t2 + " " + t3]/ Q_unigram[t2]
    uni = gamma3 * Q_unigram[t3] / sum(Q_unigram.values())
    return  tri + bi + uni


if __name__ == '__main__':
    Q_unigram, Q_bigram, Q_trigram = QMLE("../data/ass1-tagger-train")
    data = QMLE()
