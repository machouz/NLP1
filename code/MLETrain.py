from utils import *
import re

gamma1 = 0.5
gamma2 = 0.4
gamma3 = 0.1

Q_trigram = {}
Q_bigram = {}
Q_unigram = {}
E_probs = {}

len_vocabulary = 0
# Dictionary that give a compiled regex for each signature
signatures_regex = {"ed": re.compile("\w+ed$"),
                    "ing": re.compile("\w+ing$"),
                    "ent": re.compile("\w+ent$"),
                    "^Aa": re.compile("[A-Z][a-z]+"),
                    }


def replace_signature(word):
    for signature, regex in signatures_regex.items():
        if regex.match(word):
            return signature
    return word


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


def getQ(t1, t2, t3):
    tri = 0
    bi = 0
    if t1 + " " + t2 in Q_bigram:
        tri = gamma1 * Q_trigram.get(t1 + " " + t2 + " " + t3, 0) / Q_bigram.get(t1 + " " + t2)

    if t2 in Q_unigram:
        bi = gamma2 * Q_bigram.get(t2 + " " + t3, 0) / Q_unigram.get(t2, 0)

    uni = gamma3 * Q_unigram.get(t3, 0) / len_vocabulary
    return tri + bi + uni


def EMLE(fname):
    train = read_data(fname)
    for line in train:
        for word, tag in line:
            word = replace_signature(word)  # will map all the word with the same signature to the same key of E_probs
            E_probs[word + " " + tag] = E_probs.get(word + " " + tag, 0) + 1


def eFile():
    data = []
    for key, label in E_probs.items():
        data.append(key + "\t" + str(label))
    write_to_file("e.mle", data)
    return data


Q_unigram, Q_bigram, Q_trigram = QMLE("../data/ass1-tagger-train")
len_vocabulary = sum(Q_unigram.itervalues())

EMLE("../data/ass1-tagger-train")

'''
if __name__ == '__main__':
    q_data = qFile()
    e_data = eFile()
'''
