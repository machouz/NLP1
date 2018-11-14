from utils import *
import re
from datetime import datetime

start = datetime.now()

gamma1 = 0.3
gamma2 = 0.3
gamma3 = 0.4

threshold_unk = 1

Q_trigram = {}
Q_bigram = {}
Q_unigram = {}
E_probs = {}

len_vocabulary = 0

fname = "../data/ass1-tagger-train"

# Dictionary that give a compiled regex for each signature
signatures_regex = {"^ed": re.compile("\w+ed$"),
                    "^s": re.compile("\w+s$"),
                    "^ing": re.compile("\w+ing$"),
                    "^ent": re.compile("\w+ent$"),
                    "^Aa": re.compile("[A-Z][a-z]+"),
                    "^ion": re.compile("\w+ion$"),
                    "^ity": re.compile("\w+ity$"),
                    }


def replace_signature(word):
    for signature, regex in signatures_regex.items():
        if regex.match(word):
            return signature
    return word


def MLE():
    train = read_data(fname)

    for line in train:
        for a, b, c in zip(line, line[1:], line[2:]):
            tag1, tag2, tag3 = a[1], b[1], c[1]
            addQLine(tag1, tag2, tag3)
            addELine(a)

        Q_bigram[tag2 + " " + tag3] = Q_bigram.get(tag2 + " " + tag3, 0) + 1
        Q_unigram[tag2] = Q_unigram.get(tag2, 0) + 1
        Q_unigram[tag3] = Q_unigram.get(tag3, 0) + 1
        addELine(b)
        addELine(c)


    for sample, count in E_probs.items():
        word, tag = sample.split(" ")
        if count <= threshold_unk:
            sign = replace_signature(word)
            del E_probs[sample]
            if sign != word:
                E_probs[sign + " " + tag] = E_probs.get(sign + " " + tag, 0) + count
            else:
                E_probs["*UNK*" + " " + tag] = E_probs.get("*UNK*" + " " + tag, 0) + count



def addQLine(a, b, c):
    Q_unigram[a] = Q_unigram.get(a, 0) + 1
    Q_bigram[a + " " + b] = Q_bigram.get(a + " " + b, 0) + 1
    Q_trigram[a + " " + b + " " + c] = Q_trigram.get(a + " " + b + " " + c, 0) + 1

def addELine(x):
    word, tag = x
    E_probs[word + " " + tag] = E_probs.get(word + " " + tag, 0) + 1


def getQ(t1, t2, t3):
    tri = 0
    bi = 0
    if t1 + " " + t2 in Q_bigram:
        tri = gamma1 * Q_trigram.get(t1 + " " + t2 + " " + t3, 0) / Q_bigram.get(t1 + " " + t2)

    if t2 in Q_unigram:
        bi = gamma2 * Q_bigram.get(t2 + " " + t3, 0) / Q_unigram.get(t2, 0)

    uni = gamma3 * Q_unigram.get(t3, 0) / len_vocabulary
    return tri + bi + uni


def getE(word, tag):
    sign = replace_signature(word)
    if sign + " " + tag in E_probs:
        return float(E_probs[sign + " " + tag]) / Q_unigram[tag]
    return E_probs.get("*UNK*" + " " + tag, 0.0) / Q_unigram[tag]


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


def eFile():
    data = []
    for key, label in E_probs.items():
        data.append(key + "\t" + str(label))
    write_to_file("e.mle", data)
    return data


MLE()
len_vocabulary = sum(Q_unigram.itervalues())

#if __name__ == '__main__':
q_data = qFile()
e_data = eFile()

end = datetime.now()
zman = end - start
print(zman)
